from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry(SQLModel, table=True):
    __tablename__ = "log_entry"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: str = Field(default="")
    caller: str = Field(default="")
    level: LogLevel = Field(default=LogLevel.INFO)
