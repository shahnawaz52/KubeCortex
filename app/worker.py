from app.queue.redis_queue import dequeue_incident
from app.services.incident_processor import process_incident

def run_worker() -> None:
    print("Worker started, waiting for incidents jobs...")

    while True:
        try:
            incident_id = dequeue_incident()
            if incident_id is None:
                continue
            process_incident(incident_id)
        except Exception as exc:
            print(f"Error processing incident job: {str(exc)}")

if __name__ == "__main__":
    run_worker()
