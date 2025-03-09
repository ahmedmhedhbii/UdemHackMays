import uuid
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from __future__ import annotations

class NotificationType(str, Enum):
    message = "message"
    consultation = "consultation"
    analysis = "analysis"

class Notification(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    doctor_id: uuid.UUID = Field(foreign_key="doctor.id")
    type: NotificationType
    content: Optional[str] = None  # Contenu du message ou détails
    pdf_url: Optional[str] = None  # Pour stocker l'URL d'un fichier PDF d'analyse
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relation
    doctor: Optional["Doctor"] = Relationship(back_populates="notifications")
