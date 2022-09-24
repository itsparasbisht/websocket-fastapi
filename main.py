from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{client}")
async def websocket_endpoint(websocket: WebSocket, client: str):
    await manager.connect(websocket)
    joinedDict = {
        "joined" : True,
        "message" :  f'"{client.upper()} has joined the chat"'
    }
    await manager.broadcast(joinedDict)

    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        leftDict = {
            "left" : True,
            "message" :  f'"{client.upper()} left the chat"'
        }
        await manager.broadcast(leftDict)


