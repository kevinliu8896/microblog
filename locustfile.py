from locust import HttpUser, between, task
import random, string, requests

rand_usr = lambda l: ''.join(random.choices(string.ascii_letters, k=l))

class MicroblogUser(HttpUser):
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessionID = None

    def on_start(self):
        self.username, self.password = self.credentials()
        email = f"{self.username}@example.com"
        reg_data = {"username": self.username, "email": email, "password": self.password, "password2": self.password}
        log_data = {"username": self.username, "password": self.password}

        with self.client.post("/auth/register", data=reg_data, catch_response=True) as res1:
            if res1.status_code != 200:
                res1.failure(f"Failed to register. Response code: {res1.status_code}")

        with self.client.post("/auth/login-api", json=log_data, catch_response=True) as res2:
            if res2.status_code == 200:
                self.sessionID = res2.json()["session"]
            else:
                res2.failure(f"Failed to login. Response code: {res2.status_code}")

    def credentials(self):
        return rand_usr(8), "test"

    # Removed other tasks and left only the view_profile task
    @task
    def view_profile(self):
        self.client.get(f"/user/{self.username}")
