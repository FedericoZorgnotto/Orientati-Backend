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
            token = data.split("Authorization: Bearer ")[1] if "Authorization: Bearer " in data else None
            if not token:
                await websocket.close(code=3000)
                return
            user = None
            try:
                user = self.get_user_from_token(token)
                if not user:
                    await websocket.close(code=3000)
            except Exception as e:
                print(e)
                await websocket.close(code=3000)

            role = "admin" if user.admin else "users"
            self.active_connections[role][user.id] = websocket
            print(f"Nuova connessione {role}: {user.id}")
            await websocket.send_text("connected")
        except WebSocketDisconnect:
            print("WebSocket chiuso")

    def disconnect(self, user_id: str, role: str):
        """Rimuove una connessione chiusa"""
        self.active_connections[role].pop(user_id, None)
        print(f"Connessione chiusa {role}: {user_id}")

    def disconnect_websocket(self, websocket: WebSocket):
        """Rimuove una connessione chiusa"""
        for role, connections in self.active_connections.items():
            for user_id, conn in connections.items():
                if conn == websocket:
                    self.active_connections[role].pop(user_id, None)
                    print(f"Connessione chiusa {role}: {user_id}")
                    return
        print("WebSocket chiuso")

    async def send_message(self, user_id: str, message: str, role: str):
        """Invia un messaggio a un utente specifico"""
        if user_id in self.active_connections[role]:
            await self.active_connections[role][user_id].send_text(message)

    async def broadcast(self, message: str, role: str):
        """Invia un messaggio a tutti gli utenti di un certo ruolo"""
        for user_id, websocket in list(self.active_connections[role].items()):
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(user_id, role)
            except RuntimeError as e:
                self.disconnect(user_id, role)

    def get_user_from_token(self, token: str):
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
            return user
        except JWTError:
            raise credentials_exception


websocket_manager = WebSocketManager()
