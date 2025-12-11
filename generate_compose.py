import yaml

NUM_WORKERS = 12  

services = {}
for i in range(1, NUM_WORKERS + 1):
    services[f"worker{i}"] = {
        "build": {"context": "./worker"},
        "container_name": f"worker{i}",
        "ports": [f"{8000+i}:8000"],
        "networks": ["parallel_net"]
    }

services["coordinator"] = {
    "build": {"context": "./coordinator"},
    "container_name": "coordinator",
    "depends_on": [f"worker{i}" for i in range(1, NUM_WORKERS + 1)],
    "networks": ["parallel_net"],
    "environment": {"WORKERS": ",".join([f"http://worker{i}:8000" for i in range(1, NUM_WORKERS + 1)])},
    "command": ["python", "coordinator.py"]
}

compose_dict = {
    "version": "3.9",
    "services": services,
    "networks": {"parallel_net": {"driver": "bridge"}}
}

with open("docker-compose.yml", "w") as f:
    yaml.dump(compose_dict, f, sort_keys=False)

print("docker-compose.yml generated successfully!")
