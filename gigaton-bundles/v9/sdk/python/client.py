import requests

class GigatonOpsClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def health(self):
        return requests.get(f"{self.base_url}/api/health").json()

    def ready(self):
        return requests.get(f"{self.base_url}/api/ready").json()

    def get_memory_registry(self):
        return requests.get(f"{self.base_url}/api/memory-registry").json()

    def get_namespaces(self):
        return requests.get(f"{self.base_url}/api/namespaces").json()

    def generate_namespace_draft(self, payload: dict):
        return requests.post(f"{self.base_url}/api/intake/generate-namespace", json=payload).json()

    def promote_namespace(self, payload: dict):
        return requests.post(f"{self.base_url}/api/namespaces/promote", json=payload).json()

    def transition_memory(self, payload: dict):
        return requests.post(f"{self.base_url}/api/memory/transition", json=payload).json()
