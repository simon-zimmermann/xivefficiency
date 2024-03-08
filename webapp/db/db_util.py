from sqlmodel import Session
import inspect

from webapp.db.models.LogEntry import LogEntry, LogLevel
from webapp.db import engine


def log(message: str, level: LogLevel = LogLevel.INFO):
    with Session(engine) as session:
        stk = inspect.stack()[1]
        mod = inspect.getmodule(stk[0])
        log = LogEntry(message=message, caller=f"{mod.__name__}.{stk.function}", level=level)
        session.add(log)
        session.commit()
