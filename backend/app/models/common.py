from sqlmodel import SQLModel
from __future__ import annotations

# Generic message
class Message(SQLModel):
    message: str
