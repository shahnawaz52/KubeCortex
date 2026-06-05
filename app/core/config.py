import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]
INCIDENT_QUEUE_NAME = os.getenv("INCIDENT_QUEUE_NAME", "incident_jobs")
