import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from __future__ import annotations

class Patient(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True, index=True)
    date_of_birth: Optional[str] = Field(default=None, max_length=10)  # format "YYYY-MM-DD"
    
    # Chaque patient est associé à un médecin
    doctor_id: uuid.UUID = Field(foreign_key="doctor.id")
    doctor: Optional["Doctor"] = Relationship(back_populates="patients")
    
    # Relation avec les messages échangés
    messages: List["Message"] = Relationship(back_populates="patient")
