import json
from redis import Redis
from app.core.config import REDIS_URL, INCIDENT_QUEUE_NAME

_redis_client: Redis | None = None

def get_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_timeout=10,
            socket_connect_timeout=5,
        )
    return _redis_client

def enqueue_incident(incident_id: int) -> None:
    client = get_redis_client()
    payload = json.dumps({"incident_id": incident_id})
    client.lpush(INCIDENT_QUEUE_NAME, payload)

def dequeue_incident(timeout: int = 5) -> dict | None:
    client = get_redis_client()
    result = client.brpop(INCIDENT_QUEUE_NAME, timeout=timeout)
    if result is None:
        return None
    _, payload = result
    job = json.loads(payload)
    return int(job["incident_id"])
