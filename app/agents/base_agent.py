from sqlalchemy.orm import Session
from ..models import AgentLog

class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def log(self, db: Session, action_type: str, status: str, details: str):
        entry = AgentLog(
            agent_name=self.name,
            action_type=action_type,
            status=status,
            details=details
        )
        db.add(entry)
        db.commit()
