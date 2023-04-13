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

    @task(10)
    def view_homepage(self):
        with self.client.get("/index", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Failed to view homepage. Response code: {resp.status_code}")

    @task(5)
    def create_post(self):
        headers, form_data = {"Content-Type": "application/json"}, {"post": "Hello from Locust!", "submit": "Submit"}
        with self.client.post("/index-api", headers=headers, json=form_data, cookies={"session": self.sessionID}, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Failed to create post. Response code: {resp.status_code}")

    @task(2)
    def view_profile(self):
        self.client.get(f"/user/{self.username}")

    @task(3)
    def view_archive(self):
        with self.client.get("/archive-api", cookies={"session": self.sessionID}, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Failed to view archive. Response code: {resp.status_code}")

    @task(4)
    def create_and_like_post(self):
        headers, form_data = {"Content-Type": "application/json"}, {"body": "Hello from Locust!"}
        with self.client.post("/create-like-post-api", headers=headers, json=form_data, cookies={"session": self.sessionID}, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Failed to create and like post. Response code: {resp.status_code}")

    @task(1)
    def enable_disable_2fa(self):
        enable_2fa = random.choice([True, False])
        headers, form_data = {"Content-Type": "application/json"}, {"authentication": "yes" if enable_2fa else "no"}
        with self.client.post("/auth/manage_authentication_api", headers=headers, json=form_data, cookies={"session": self.sessionID}, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Failed to enable/disable 2FA. Response code: {resp.status_code}")