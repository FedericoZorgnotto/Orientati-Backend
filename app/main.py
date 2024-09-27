from importlib.metadata import version

from fastapi import FastAPI
# from app.routers.v1 import auth, users
from app.config import settings
from fastapi_versioning import VersionedFastAPI, version


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


# app.include_router(auth.router, prefix="/api/v1")
# app.include_router(users.router, prefix="/api/v1")

@app.get("/")
@version(1, 0)
async def read_root():
    """
    This is the root path of the API

    It will return a welcome message
    """
    return {"message": f"Welcome to {settings.app_name}"}


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')
