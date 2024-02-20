from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 3)  # Время ожидания между запросами

    @task
    def add_stats(self):
        self.client.post("/stats/", json={"device_id": 1, "x": 1, "y": 2, "z": 3, "date": "2000-01-01"})

