import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from __future__ import annotations

class Doctor(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True, index=True)
    specialty: Optional[str] = Field(default=None, max_length=255)
    
    # Relations
    patients: List["Patient"] = Relationship(back_populates="doctor")
    messages: List["Message"] = Relationship(back_populates="doctor")
    notifications: List["Notification"] = Relationship(back_populates="doctor")
