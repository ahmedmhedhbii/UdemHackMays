from datetime import datetime
import uuid

from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, Column, LargeBinary
from typing import Optional

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    # For doctors:
    specialization: str | None = Field(default=None, max_length=255)
    # For patients:
    date_of_birth: str | None = Field(default=None, max_length=10)
    # For patients: assign a doctor (if known)
    doctor_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    # Extra fields that apply based on role:
    specialization: str | None = Field(default=None, max_length=255)  # only for doctors
    date_of_birth: str | None = Field(default=None, max_length=10)  # only for patients
    doctor_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")

    # Relationship: if this user is a patient, the 'doctor' relationship points to a doctor record.
    doctor: Optional["User"] = Relationship(
        back_populates="patients",
        sa_relationship_kwargs={"remote_side": "User.id"}
    )
    # If this user is a doctor, this will list all their patient users.
    patients: list["User"] = Relationship(
        back_populates="doctor",
        sa_relationship_kwargs={"foreign_keys": "[User.doctor_id]"}
    )
    # Appointments where the user is the patient.
    appointments_as_patient: list["Appointment"] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={"foreign_keys": "[Appointment.patient_id]"}
    )
    # Appointments where the user is the doctor.
    appointments_as_doctor: list["Appointment"] = Relationship(
        back_populates="doctor",
        sa_relationship_kwargs={"foreign_keys": "[Appointment.doctor_id]"}
    )
    # A patient can have many medical records.
    medical_records: list["MedicalRecord"] = Relationship(back_populates="patient")
    # Other relationships (e.g., items)
    items: list["Item"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "delete"})

    # Nouvelle relation : Notifications pour le médecin
    notifications: list["Notification"] = Relationship(back_populates="doctor")



# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


##################################################
# Appointment model linking patients and doctors #
##################################################
class Appointment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    patient_id: uuid.UUID = Field(foreign_key="user.id")
    doctor_id: uuid.UUID = Field(foreign_key="user.id")
    appointment_date: str = Field(max_length=19)  # Format "YYYY-MM-DD HH:MM:SS"
    reason: str | None = Field(default=None, max_length=255)

    # Relationships
    patient: User | None = Relationship(
        back_populates="appointments_as_patient",
        sa_relationship_kwargs={"foreign_keys": "[Appointment.patient_id]"}
    )
    doctor: User | None = Relationship(
        back_populates="appointments_as_doctor",
        sa_relationship_kwargs={"foreign_keys": "[Appointment.doctor_id]"}
    )


# MedicalRecord now stores a PDF resume and a scanner image (as file paths, URLs, or similar)
class MedicalRecord(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    patient_id: uuid.UUID = Field(foreign_key="user.id")
    record_date: str = Field(max_length=10)  # Format "YYYY-MM-DD"
    description: str = Field(max_length=1024)
    pdf_resume: bytes | None = Field(default=None, sa_column=Column(LargeBinary))
    scanner_image: bytes | None = Field(default=None, sa_column=Column(LargeBinary))
    patient: User | None = Relationship(back_populates="medical_records")

class TranslationRequest(SQLModel):
    input_str: str

class Notification(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    doctor_id: uuid.UUID = Field(foreign_key="user.id")
    type: str = Field(max_length=50)  # ex: "message", "consultation", "analysis"
    content: Optional[str] = None  # Détails de la notification
    pdf_url: Optional[str] = None  # Pour un résultat d'analyse en PDF
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relation : Le médecin auquel appartient la notification
    doctor: Optional["User"] = Relationship(back_populates="notifications")
