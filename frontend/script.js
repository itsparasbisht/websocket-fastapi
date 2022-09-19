let ws = new WebSocket("ws://localhost:8000/ws");
let btn = document.getElementById("sendData");
let input = document.querySelector("input");

const handleData = () => {
  ws.send(input.value);
};

btn.addEventListener("click", handleData);

ws.onopen = () => ws.send("connected to frontend");
ws.onmessage = (e) => console.log(e.data);
