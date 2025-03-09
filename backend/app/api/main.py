from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, doctor_dashboard
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(doctor_dashboard.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)

from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
app.include_router(api_router, prefix=settings.API_V1_STR)
