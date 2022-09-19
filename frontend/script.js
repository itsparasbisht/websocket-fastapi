let ws = new WebSocket("ws://localhost:8000/ws");
ws.onopen = () => ws.send("connected to frontend");
ws.onmessage = (e) => console.log(e.data);
