from django.test import Client
from django.contrib.auth import get_user_model
import logging

LOGGER = logging.getLogger(__name__)
User = get_user_model()

def run():
    client = Client()
    user = User.objects.get(email="nathaniel.charbonneau@L3Harris.com")
    client.force_login(user=user)

    response = client.post(
        "/v1/program-review-tool/job-run",
        data={"job_name": "test"},
        content_type="application/json",
    )
    LOGGER.info(f"POST Status: {response.status_code}")
    LOGGER.info(f"POST Body: {response.content.decode()}")

    response = client.get(
        "/v1/program-review-tool/job-run",
        content_type="application/json"
    )
    LOGGER.info(f"GET Status: {response.status_code}")
    LOGGER.info(f"GET Body: {response.content.decode()}")
    LOGGER.info(f"GET response {response}")

    response = client.get(
        "/v1/program-review-tool/job-run/registry"
    )
    LOGGER.info(f"GET Status: {response.status_code}")
    LOGGER.info(f"GET Body: {response.content.decode()}")
    LOGGER.info(f"GET response {response}")
