from app.db.base import Base
from app.db.session import engine
from app.db.models.incident import Incident
from app.db.models.investigation_step import InvestigationStep


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
