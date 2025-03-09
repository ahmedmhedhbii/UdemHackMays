from __future__ import annotations
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from app.core.db import get_session
from app.models import Notification, User, Message
from app.api.deps import get_current_active_doctor

router = APIRouter(prefix="/doctor", tags=["doctor"])


@router.get("/notifications", response_model=List[Notification])
def get_notifications(
    session: Session = Depends(get_session),
    current_doctor: User = Depends(get_current_active_doctor)
):
    """
    Récupère toutes les notifications du médecin connecté.
    """
    statement = select(Notification).where(Notification.doctor_id == current_doctor.id)
    notifications = session.exec(statement).all()
    return notifications


@router.get("/patients", response_model=List[User])
def search_patients(
    q: Optional[str] = None,
    session: Session = Depends(get_session),
    current_doctor: User = Depends(get_current_active_doctor)
):
    """
    Recherche des patients associés au médecin connecté par nom ou email.
    """
    statement = select(User).where(User.doctor_id == current_doctor.id)
    if q:
        # Recherche case-insensitive dans full_name et email
        statement = statement.where(
            User.full_name.ilike(f"%{q}%") | User.email.ilike(f"%{q}%")
        )
    patients = session.exec(statement).all()
    return patients


@router.get("/messages", response_model=List[Message])
def get_message_history(
    patient_id: Optional[uuid.UUID] = None,
    session: Session = Depends(get_session),
    current_doctor: User = Depends(get_current_active_doctor)
):
    """
    Récupère l'historique des messages du médecin connecté.
    Optionnellement, filtre par identifiant de patient.
    """
    statement = select(Message).where(Message.doctor_id == current_doctor.id)
    if patient_id:
        statement = statement.where(Message.patient_id == patient_id)
    messages = session.exec(statement).all()
    return messages


@router.post("/llm/analyze", response_model=dict)
def analyze_patient_data(
    patient_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_doctor: User = Depends(get_current_active_doctor)
):
    """
    Simule l'appel à un module LLM pour analyser des données médicales (OCR, scans, etc.).
    Renvoie un résultat fictif.
    """
    # Ici, tu appellerais ton modèle LLM ou tes services d'analyse.
    # Pour l'exemple, on renvoie un résultat simulé.
    analysis_result = {
        "patient_id": str(patient_id),
        "analysis": "Simulated LLM analysis result: All metrics are within normal ranges.",
        "timestamp": datetime.utcnow().isoformat()
    }
    return analysis_result


@router.post("/messages/send", response_model=Message)
def send_message(
    patient_id: uuid.UUID,
    content: str,
    session: Session = Depends(get_session),
    current_doctor: User = Depends(get_current_active_doctor)
):
    """
    Envoie un message du médecin à un patient.
    Ce message pourrait contenir la réponse générée par le LLM.
    """
    new_message = Message(
        doctor_id=current_doctor.id,
        patient_id=patient_id,
        content=content,
        sent_at=datetime.utcnow().isoformat()
    )
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return new_message
