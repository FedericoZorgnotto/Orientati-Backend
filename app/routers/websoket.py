from fastapi import APIRouter, WebSocket

from app.websocket_manager import websocket_manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except Exception as e:
        print(f"Errore durante la ricezione del messaggio: {e}")
        websocket_manager.disconnect_websocket(websocket)
