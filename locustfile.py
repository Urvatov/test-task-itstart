from locust import HttpUser, task, between

#locust -f locustfile.py

class TestUser(HttpUser):
    wait_time = between(1, 3)  # Время ожидания между запросами

    @task
    def add_user(self):
        self.client.post("/users/", json={"name" : "test_user"})
    
    @task
    def add_device(self):
        self.client.post("/devices/", json={"name" : "test_device", "user_id" : 1})

    @task
    def add_stats(self):
        self.client.post("/stats/", json={"device_id": 1, "x": 1, "y": 2, "z": 3, "date": "2000-01-01"})

    @task
    def get_stats_by_device(self):
        self.client.get("/stats/1")

    @task
    def get_analysis_by_device(self):
        self.client.get("/stats/analysis/?device_id=1")

    @task
    def get_analysis_by_user(self):
        self.client.get("/users/analysis/?user_id=1")