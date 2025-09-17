from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4, UUID
from typing import Dict, Any


class ReportType(Enum):
    LACKED_AUTHORITY = "lacked_authority"
    EXPECTED_INITIATIVE = "expected_initiative"


@dataclass(frozen=True)
class Report:
    user_id: str
    workspace_id: str
    report_type: ReportType
    description: str
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "workspace_id": self.workspace_id,
            "report_type": self.report_type.value,
            "description": self.description,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Report":
        return cls(
            id=UUID(data["id"]),
            user_id=data["user_id"],
            workspace_id=data["workspace_id"],
            report_type=ReportType(data["report_type"]),
            description=data["description"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
    
    def __str__(self) -> str:
        return (
            f"Report by {self.user_id} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}: "
            f"{self.report_type.value}"
        )