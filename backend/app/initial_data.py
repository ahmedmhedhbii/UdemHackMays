import logging
from sqlmodel import Session, select
from app.core.db import engine, init_db
from app.models import User, UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)

def populate_db() -> None:
    with Session(engine) as session:
        # Créer un docteur de test s'il n'existe pas
        doctor = session.exec(
            select(User).where(User.email == "doctor@example.com")
        ).first()
        if not doctor:
            logger.info("Creating test doctor data")
            doctor_in = UserCreate(
                email="doctor@example.com",
                password="password123",  # Le mot de passe sera hashé dans la logique de création
                full_name="Doctor Test",
                specialization="Cardiology",  # Champ renseigné pour indiquer que c'est un docteur
                date_of_birth=None,  # Non pertinent pour un docteur
                doctor_id=None
            )
            from app import crud
            doctor = crud.create_user(session=session, user_create=doctor_in)
            session.commit()
            logger.info(f"Test doctor created with id: {doctor.id}")
        else:
            logger.info("Test doctor already exists")
        
        # Créer un patient de test s'il n'existe pas
        patient = session.exec(
            select(User).where(User.email == "patient@example.com")
        ).first()
        if not patient:
            logger.info("Creating test patient data")
            patient_in = UserCreate(
                email="patient@example.com",
                password="password123",
                full_name="Patient Test",
                date_of_birth="1990-01-01",
                doctor_id=doctor.id
            )
            patient = crud.create_user(session=session, user_create=patient_in)
            session.commit()
            logger.info(f"Test patient created with id: {patient.id}")
        else:
            logger.info("Test patient already exists")

def main() -> None:
    logger.info("Creating initial data")
    init()
    populate_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
