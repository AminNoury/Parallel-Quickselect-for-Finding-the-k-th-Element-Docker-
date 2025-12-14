const arrayContainer = document.getElementById("arrayContainer");
const stepsContainer = document.getElementById("stepsContainer");
const startBtn = document.getElementById("startBtn");
const arraySizeInput = document.getElementById("arraySize");
const kInput = document.getElementById("k");

startBtn.addEventListener("click", async () => {
    const size = parseInt(arraySizeInput.value);
    const k = parseInt(kInput.value);



    // ---- VALIDATION ----
    if (isNaN(size) || size < 4 || size > 1000) {
        alert("Array size must be between 4 and 1000.");
        return;
    }

    if (isNaN(k) || k < 1 || k >= size) {
    alert("k must be at least 1 and smaller than array size.");
    return;
    }

    // if (isNaN(size) || size < 4) {
    //     alert("Array size must be at least 4 (because we use 4 chunks).");
    //     return;
    // }

    // if (isNaN(k) || k < 1 || k >= size) {
    //     alert("k must be at least 1 and strictly less than array size (k < n).");
    //     return;
    // }


    const originalArr = Array.from({length: size}, () => Math.floor(Math.random() * 100) + 1);
    let arr = originalArr.slice();
    let currentK = k;

    stepsContainer.innerHTML = "";
    arrayContainer.innerHTML = "";


    arrayContainer.innerHTML = `<div class="array-box"><strong>Initial Array:</strong> ${originalArr.map(v => `<span>${v}</span>`).join(" ")}</div>`;

    let step = 1;
    let kthElement = null;

    while (arr.length > 0) {
        const pivot = arr[Math.floor(Math.random() * arr.length)];

        const chunks = [];
        const workers = 4;
        const chunkSize = Math.ceil(arr.length / workers);
        for (let i = 0; i < arr.length; i += chunkSize) {
            chunks.push(arr.slice(i, i + chunkSize));
        }

        const results = chunks.map(chunk => {
            const less = chunk.filter(x => x < pivot);
            const equal = chunk.filter(x => x === pivot);
            const greater = chunk.filter(x => x > pivot);
            return {chunk, less, equal, greater};
        });


        const stepDiv = document.createElement("div");
        stepDiv.className = "step";
        stepDiv.innerHTML = `<h3>Step ${step} - Pivot: ${pivot}</h3>`;
        results.forEach((r,i)=>{
            stepDiv.innerHTML += `
            <div class="worker-box">
                <strong>Worker ${i+1}</strong>
                <div>Chunk: [${r.chunk.join(", ")}]</div>
                <div>less: [${r.less.join(", ")}]</div>
                <div>equal: [${r.equal.join(", ")}]</div>
                <div>greater: [${r.greater.join(", ")}]</div>
            </div>`;
        });
        stepsContainer.appendChild(stepDiv);

        const lessTotal = results.reduce((sum,r)=>sum+r.less.length,0);
        const equalTotal = results.reduce((sum,r)=>sum+r.equal.length,0);

        if (currentK <= lessTotal) {
            arr = arr.filter(x => x < pivot);
        } else if (currentK <= lessTotal + equalTotal) {
            kthElement = pivot;
            break;
        } else {
            arr = arr.filter(x => x > pivot);
            currentK -= (lessTotal + equalTotal);
        }

        if(arr.length === 1){
            kthElement = arr[0];
            break;
        }

        step++;
        await new Promise(r => setTimeout(r, 600));
    }

    const sortedArr = originalArr.slice().sort((a,b)=>a-b);
    const kthIndex = k-1;
    const sortedDiv = document.createElement("div");
    sortedDiv.className = "sorted-array";
    sortedDiv.innerHTML = `<strong>Sorted Array:</strong> ${sortedArr.map((v,i) => i===kthIndex ? `<span class="kth-element">${v}</span>` : `<span>${v}</span>`).join(" ")}`;
    arrayContainer.appendChild(sortedDiv);

    stepsContainer.innerHTML += `<div class="step final"><h3>Found k-th element: <span class="kth-element">${kthElement}</span></h3></div>`;
});
