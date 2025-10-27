import { io } from "socket.io-client";

// Replace with your backend URL (use localhost:5000 for local testing)
const SOCKET_URL = "http://localhost:5000";

const socket = io(SOCKET_URL, {
  transports: ["websocket"],  // Ensures fast connection
  withCredentials: true
});

export default socket;
