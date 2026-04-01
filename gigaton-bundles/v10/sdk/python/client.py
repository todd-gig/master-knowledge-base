import requests

class GigatonOpsClient:
    def __init__(self, base_url: str, tenant_id: str):
        self.base_url = base_url.rstrip("/")
        self.tenant_id = tenant_id

    def _headers(self):
        return {"x-tenant-id": self.tenant_id}

    def health(self):
        return requests.get(f"{self.base_url}/api/health").json()

    def ready(self):
        return requests.get(f"{self.base_url}/api/ready").json()

    def get_memory_registry(self):
        return requests.get(f"{self.base_url}/api/memory-registry").json()

    def get_namespaces(self):
        return requests.get(f"{self.base_url}/api/namespaces", headers=self._headers()).json()

    def generate_namespace_draft(self, payload: dict):
        return requests.post(f"{self.base_url}/api/intake/generate-namespace", json=payload, headers=self._headers()).json()

    def promote_namespace(self, payload: dict):
        return requests.post(f"{self.base_url}/api/namespaces/promote", json=payload, headers=self._headers()).json()

    def transition_memory(self, payload: dict):
        return requests.post(f"{self.base_url}/api/memory/transition", json=payload, headers=self._headers()).json()

    def emit_billing_event(self, payload: dict):
        return requests.post(f"{self.base_url}/api/billing/events", json=payload, headers=self._headers()).json()
