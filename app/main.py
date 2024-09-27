from fastapi import FastAPI
# from app.routers.v1 import auth, users
from app.config import settings

app = FastAPI()


# Includi i router
# app.include_router(auth.router, prefix="/api/v1")
# app.include_router(users.router, prefix="/api/v1")

# Un semplice endpoint di test
@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.app_name}"}
