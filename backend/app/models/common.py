from sqlmodel import SQLModel

# Exemple de message générique
class Message(SQLModel):
    message: str
