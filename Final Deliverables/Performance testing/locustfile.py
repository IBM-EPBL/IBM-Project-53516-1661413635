import time
from locust import HttpUser, task, between


class WebsiteTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get(url="http://127.0.0.1:5000")
