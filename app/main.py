from fastapi import FastAPI, Request, Response
from fastapi_versioning import VersionedFastAPI, version
import sentry_sdk

from app.config import settings
from app.routers.v1 import auth
from app.routers.v1.admin import admin

description = """
This is the API for the Vallauri orientamento project.
# Root
The API root is located at `/`, it responses with a welcome message.
## Authentication
The API uses JWT for authentication. You can obtain a token by sending a POST request to `/api/v1/auth/login`.
"""

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title=settings.app_name,
    description=description,
    version=settings.version
)

app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")

@app.get("/sentry-debug")
@version(1, 0)
async def trigger_error():
    division_by_zero = 1 / 0
@app.get("/")
@version(1, 0)
async def read_root():
    """
    path di root dell'API

    restituisce un messaggio di benvenuto
    """
    return {"message": f"Welcome to {settings.app_name}"}


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')


@app.middleware("http")
async def cors_handler(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response
