# Parallel-Quickselect-for-Finding-the-k-th-Element-Docker-
This project implements the Parallel Quickselect algorithm to efficiently find the k-th smallest element in an unsorted array. Instead of running Quickselect sequentially on a single CPU core, the algorithm distributes the partition step across multiple Workers running inside Docker containers, allowing parallel executi

# Parallel Quickselect for Finding the k-th Element (Docker)

## Contributors
- **Supervisor:** Dr. Javad Mohammad Zadeh
- **Developer:** Amin Nouri
- **Special Thanks:** Navid Tavasoli

---

## Overview

This project implements the **Parallel Quickselect** algorithm to efficiently find the **k-th smallest element** in an unsorted array.  
Instead of running Quickselect sequentially on a single CPU core, the algorithm distributes the partition step across multiple **Workers** running inside **Docker containers**, allowing parallel execution.  

The project also includes a **Frontend visualization** to show each step of the algorithm.

---

## Prerequisites

- Docker
- Docker Compose
- Python 3.11+ (for building images)

---

## How to Run

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <your-repo-folder>
---

2 . **Build and start Docker containers**

docker compose up --build


Build the Coordinator and Worker Docker images

Start the Coordinator on port 8000

Start Workers in separate containers

3. **Access the Frontend**

Once Docker is running, open your browser and go to:

http://localhost:8080



Here, you can:

    Set the array size

    Choose k

    Visualize the steps of the Parallel Quickselect algorithm

Architecture

    Coordinator: Selects pivot, distributes chunks, aggregates results, decides next steps.

    Workers: Each worker runs inside a Docker container, processes chunks, returns counts of less, equal, and greater.

    Frontend: Visualizes arrays and algorithm steps.

    Docker: Isolates Workers and allows parallel execution. Coordinator communicates with Workers via HTTP requests.

Ports

    Coordinator API: 8000

    Frontend: 8080

    Workers: internal, accessed by Coordinator

Example Usage

    Open the frontend at http://localhost:8080

    Enter array size (e.g., 15)

    Enter k (e.g., 3)

    Click Start to run the algorithm and watch each step.

Notes

    Each Worker can be pinned to 1 CPU core using Docker Compose.

    The number of Workers can be adjusted in the docker-compose.yml.

    This project demonstrates parallel processing with Docker for selection algorithms.


