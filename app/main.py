from fastapi import FastAPI, Depends

from app.config import settings
from fastapi_versioning import VersionedFastAPI, version

from app.routers.v1 import auth
from app.routers.v1.admin.admin import admin_router

description = """
This is the API for the Vallauri orientamento project.
# Root 
The API root is located at `/`, it responses with a welcome message.
## Authentication
The API uses JWT for authentication. You can obtain a token by sending a POST request to `/api/v1/auth/login`.


"""

app = FastAPI(
    title=settings.app_name,
    description=description,
    version=settings.version

)


app.include_router(auth.router)
app.include_router(admin_router, prefix="/admin")
@app.get("/")
@version(1, 0)
async def read_root():
    """
    path di root dell'API

    restituisce un messaggio di benvenuto
    """
    return {"message": f"Welcome to {settings.app_name}"}


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')

