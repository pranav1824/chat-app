import React, { useEffect, useState, useContext } from "react";
import io from "socket.io-client";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

const socket = io("http://127.0.0.1:5000");

const Chat = () => {
  const { token, user } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    // Authenticate socket with JWT
    socket.emit("authenticate", { token });

    // Load past messages
    const fetchMessages = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/chat/messages", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMessages(res.data);
      } catch (err) {
        console.error("Error fetching messages:", err);
      }
    };
    fetchMessages();

    // Listen for new messages
    socket.on("new_message", (msg) => {
      setMessages((prev) => [...prev, msg]);
    });

    return () => {
      socket.off("new_message");
    };
  }, [token]);

  const sendMessage = () => {
    if (input.trim()) {
      socket.emit("send_message", { token, content: input });
      setInput("");
    }
  };

  return (
    <div className="chat-container" style={{ maxWidth: 600, margin: "auto", marginTop: 50 }}>
      <h2>Welcome, {user?.username}</h2>
      <div
        className="chat-box"
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          height: "400px",
          overflowY: "auto",
          marginBottom: "10px",
        }}
      >
        {messages.map((m, i) => (
          <div key={i}>
            <b>{m.sender}</b>: {m.content}
          </div>
        ))}
      </div>

      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        placeholder="Type a message..."
        style={{ width: "80%", padding: "8px" }}
      />
      <button onClick={sendMessage} style={{ padding: "8px 12px", marginLeft: "5px" }}>
        Send
      </button>
    </div>
  );
};

export default Chat;
