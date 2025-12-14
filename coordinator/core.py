# import requests
# import random
# import math

# workers = [
#     "http://worker1:8000",
#     "http://worker2:8000"
# ]

# def quickselect_parallel(arr: list[int], k: int):
#     if not arr or not 1 <= k <= len(arr):
#         raise ValueError("Invalid array or k")

#     steps = []            # <-- برای frontend

#     step_number = 1
#     original_arr = arr[:]  # save for logging

#     while True:
#         if len(arr) == 1:
#             return {"result": arr[0], "steps": steps}

#         pivot = random.choice(arr)

#         active_workers = min(len(workers), len(arr))
#         chunk_size = math.ceil(len(arr) / active_workers)
#         chunks = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]

#         results = []   # برای frontend
#         less_total = equal_total = greater_total = 0

#         for i, worker in enumerate(workers):
#             if i >= len(chunks): break
#             chunk = chunks[i]
#             if not chunk: continue

#             r = requests.post(worker + "/partition",
#                               json={"chunk": chunk, "pivot": pivot},
#                               timeout=3).json()

#             results.append({
#                 "worker": worker,
#                 "chunk": chunk,        
#                 "less": r["less"],
#                 "equal": r["equal"],
#                 "greater": r["greater"],
#             })

#             less_total += r["less"]
#             equal_total += r["equal"]
#             greater_total += r["greater"]

#         # ذخیره‌ی مرحله
#         steps.append({
#             "step": step_number,
#             "pivot": pivot,
#             "workers": results,
#             "less_total": less_total,
#             "equal_total": equal_total,
#             "greater_total": greater_total,
#             "current_array": arr[:],
#         })
#         step_number += 1

  
#         if k <= less_total:
#             arr = [x for x in arr if x < pivot]
#         elif k <= less_total + equal_total:
#             return {"result": pivot, "steps": steps}
#         else:
#             k -= (less_total + equal_total)
#             arr = [x for x in arr if x > pivot]

import requests
import random
import math

workers = [
    "http://worker1:8000",
    "http://worker2:8000",
    "http://worker3:8000",
    "http://worker4:8000",
]

def quickselect_parallel(arr: list[int], k: int):
    if not arr or not 1 <= k <= len(arr):
        raise ValueError("Invalid array or k")

    if not arr or len(arr) < 4:
        raise ValueError("Array size must be at least 4 (4 chunks required)")

    if k < 1 or k >= len(arr):
        raise ValueError("k must satisfy 1 ≤ k < len(array)")

    if not all(isinstance(x, int) for x in arr):
        raise ValueError("Array elements must be integers")


    steps = []
    step_number = 1
    original_arr = arr[:]

    while True:
        if len(arr) == 1:
            return {"result": arr[0], "steps": steps}

        pivot = random.choice(arr)

        active_workers = min(len(workers), len(arr))
        chunk_size = math.ceil(len(arr) / active_workers)
        chunks = [arr[i:i+chunk_size] for i in range(0, len(arr), chunk_size)]

        results = []
        less_total = equal_total = greater_total = 0

        for i, worker in enumerate(workers):
            if i >= len(chunks):
                break
            chunk = chunks[i]
            if not chunk:
                continue

            r = requests.post(worker + "/partition",
                              json={"chunk": chunk, "pivot": pivot},
                              timeout=3).json()

            results.append({
                "worker": worker,
                "chunk": chunk,
                "less": r["less"],
                "equal": r["equal"],
                "greater": r["greater"],
            })

            less_total += r["less"]
            equal_total += r["equal"]
            greater_total += r["greater"]

        steps.append({
            "step": step_number,
            "pivot": pivot,
            "workers": results,
            "less_total": less_total,
            "equal_total": equal_total,
            "greater_total": greater_total,
            "current_array": arr[:],
        })
        step_number += 1

        if k <= less_total:
            arr = [x for x in arr if x < pivot]
        elif k <= less_total + equal_total:
            return {"result": pivot, "steps": steps}
        else:
            k -= (less_total + equal_total)
            arr = [x for x in arr if x > pivot]
