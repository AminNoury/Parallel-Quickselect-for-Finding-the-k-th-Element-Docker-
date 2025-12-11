from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from core import quickselect_parallel
import random

app = FastAPI(title="Parallel Quickselect Coordinator")

# Optional: serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class KSelectRequest:
    # for API endpoint if using JSON post
    pass

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("frontend/index.html", "r") as f:  
        return f.read()
    
@app.post("/compute", response_class=HTMLResponse)
async def compute(array_size: int = Form(...), k: int = Form(...)):
    arr = [random.randint(1, 100) for _ in range(array_size)]
    result = quickselect_parallel(arr, k)

    # Pass result to frontend through JSON script
    script_data = f"""
        <script>
            window.selectionData = {result};
        </script>
    """

    with open("frontend/index.html") as f:
        html = f.read()

    return HTMLResponse(script_data + html)

@app.get("/health")
def health():
    return {"status": "ok"}
