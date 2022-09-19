from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Accepting connection...")
    await websocket.accept()
    print("Accepted...")

    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Sending from server")
            print(data)
        except:
            break

