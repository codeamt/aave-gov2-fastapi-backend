from locust import HttpUser, task


class LoadTesting(HttpUser):
    @task
    def off_chain_briefs(self):
        self.client.post("/api/v1/hello", json={})

    @task
    def on_chain_briefs(self):
        self.client.post("/api/v1/hello", json={})

    @task
    def off_chain_proposal(self):
        self.client.post("/api/v1/hello", json={})

    @task
    def on_chain_proposal(self):
        self.client.post("/api/v1/hello", json={})