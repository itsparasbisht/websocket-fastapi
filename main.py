from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.get("/")
def root():
    return {"message": "initial route for chat-websocket"}

@app.websocket("/ws/{client}/{id}")
async def websocket_endpoint(websocket: WebSocket, client: str, id):
    await manager.connect(websocket)
    joinedDict = {
        "info": True,
        "joined" : True,
        "message" :  f'"{client.upper()} has joined the chat"'
    }
    await manager.broadcast(joinedDict)

    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        leftDict = {
            "info": True,
            "left" : True,
            "message" :  f'"{client.upper()} left the chat"'
        }
        await manager.broadcast(leftDict)


