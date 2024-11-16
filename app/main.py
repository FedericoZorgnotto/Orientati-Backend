from contextlib import asynccontextmanager

import sentry_sdk
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request, Response
from fastapi_versioning import VersionedFastAPI, version

from app.config import settings
from app.routers.v1 import *
from app.services.logs import log_user_action
from app.services.utentiTemporanei import elimina_utenti_temporanei

description = """
This is the API for the Vallauri orientamento project.
# Root
The API root is located at `/`, it responses with a welcome message.
## Authentication
The API uses JWT for authentication. You can obtain a token by sending a POST request to `/api/v1/auth/login`.
"""

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    # Pianifica il job per eseguire ogni giorno a mezzanotte
    scheduler.add_job(elimina_utenti_temporanei, 'cron', hour=0, minute=0)
    scheduler.start()
    yield


app = FastAPI(
    title=settings.app_name,
    description=description,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")
app.include_router(orientatore.router, prefix="/orientatore")


@app.get("/")
@version(1, 0)
async def read_root():
    """
    path di root dell'API

    restituisce un messaggio di benvenuto
    """
    from app.models.logUtente import CategoriaLogUtente
    await log_user_action(utente_id=1, azione="API root", categoria=CategoriaLogUtente.INFO)

    return {"message": f"Welcome to {settings.app_name}"}


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')


@app.middleware("http")
async def cors_handler(request: Request, call_next):
    # Gestione preflight OPTIONS
    if request.method == "OPTIONS":
        response = Response()
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response

    # Continuare con la richiesta normale
    response: Response = await call_next(request)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response
