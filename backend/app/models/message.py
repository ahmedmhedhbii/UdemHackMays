import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from __future__ import annotations

class Message(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    doctor_id: uuid.UUID = Field(foreign_key="doctor.id")
    patient_id: uuid.UUID = Field(foreign_key="patient.id")
    content: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    llm_response: Optional[str] = None  # Optionnel : réponse générée par le LLM

    # Relations
    doctor: Optional["Doctor"] = Relationship(back_populates="messages")
    patient: Optional["Patient"] = Relationship(back_populates="messages")
