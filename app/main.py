from fastapi import FastAPI

from app.api.routes.alerts import router as alerts_router
from app.api.routes.incidents import router as incidents_router

app = FastAPI(title="KubeCortex")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(alerts_router)
app.include_router(incidents_router)
