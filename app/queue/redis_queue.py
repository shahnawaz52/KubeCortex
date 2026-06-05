import json
from redis import Redis
from app.core.config import REDIS_URL, INCIDENT_QUEUE_NAME

def get_redis_client() -> Redis:
    return Redis.from_url(REDIS_URL, decode_responses=True)

def enqueue_incident(incident_id: int) -> None:
    client = get_redis_client()
    try:
        payload = json.dumps({"incident_id": incident_id})
        client.lpush(INCIDENT_QUEUE_NAME, payload)
    finally:
        client.close()

def dequeue_incident(timeout: int = 0) -> dict | None:
    client = get_redis_client()
    try:
        result = client.brpop(INCIDENT_QUEUE_NAME, timeout=timeout)
        if result is None:
            return None
        _, payload = result
        job = json.loads(payload)
        return int(job["incident_id"])
    finally:
        client.close()
