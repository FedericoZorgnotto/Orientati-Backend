from datetime import datetime
from typing import Dict

from fastapi import WebSocket, HTTPException, WebSocketDisconnect
from jose import jwt, JWTError

from app.core.config import settings
from app.database import get_db
from app.models import Utente


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {
            "users": {},  # Connessioni utenti normali
            "admin": {}  # Connessioni admin
        }

    async def connect(self, websocket: WebSocket):
        """Accetta una nuova connessione WebSocket e verifica il token di autorizzazione"""
        await websocket.accept()

        try:
            data = await websocket.receive_text()
            print(data)  # Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInVzZXJfaWQiOjEsImV4cCI6MTc0MzY2MzE5MX0.GE126C5GFccEVawe2XgJ87WMxn_UHkLBX4yKJGvdMjo
            token = data.split("Authorization: Bearer ")[1] if "Authorization: Bearer " in data else None
            if not token:
                await websocket.close(code=3000)
                return
            user = None
            try:
                user = self.admin_access(token)
            except Exception as e:
                print(e)
                await websocket.close(code=3000)
            if not user:
                await websocket.close(code=3000)

            role = "admin" if user.admin else "users"
            self.active_connections[role][user.id] = websocket
            print(f"Nuova connessione {role}: {user.id}")
            print(self.active_connections)
            await websocket.send_text("connected")
        except WebSocketDisconnect:
            print(f"WebSocket chiuso")


    def disconnect(self, user_id: str, role: str):
        """Rimuove una connessione chiusa"""
        self.active_connections[role].pop(user_id, None)
        print(f"Connessione chiusa {role}: {user_id}")

    async def send_message(self, user_id: str, message: str, role: str):
        """Invia un messaggio a un utente specifico"""
        if user_id in self.active_connections[role]:
            await self.active_connections[role][user_id].send_text(message)

    async def broadcast(self, message: str, role: str):
        """Invia un messaggio a tutti gli utenti di un certo ruolo"""
        for websocket in self.active_connections[role].values():
            await websocket.send_text(message)

    def admin_access(self, token: str):
        db = next(get_db())
        credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.now():
                raise HTTPException(status_code=401, detail="Token has expired")
            try:
                user = db.query(Utente).filter(Utente.username == username).first()
            except Exception as e:
                print(e)
                raise HTTPException(status_code=401, detail="Could not validate credentials")
            if not user or not user.admin:
                raise HTTPException(status_code=403, detail="Not enough permissions")
            return user
        except JWTError:
            raise credentials_exception


websocket_manager = WebSocketManager()
