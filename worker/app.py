from fastapi import FastAPI
from typing import List

from pydantic import BaseModel

app = FastAPI(title="QuickSelect Worker")

class PartitionRequest(BaseModel):
    chunk: list[int]
    pivot: int

class PartitionResponse(BaseModel):
    chunk: List[int]
    pivot: int
    less: List[int]
    equal: List[int]
    greater: List[int]


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/partition", response_model=PartitionResponse)
def partition(req: PartitionRequest):
    less_list = [x for x in req.chunk if x < req.pivot]
    equal_list = [x for x in req.chunk if x == req.pivot]
    greater_list = [x for x in req.chunk if x > req.pivot]

    return PartitionResponse(
        chunk=req.chunk,
        pivot=req.pivot,
        less=less_list,
        equal=equal_list,
        greater=greater_list
    )
