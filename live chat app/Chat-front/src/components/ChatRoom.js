import React, { useEffect, useState } from "react";
import socket from "../socket";

const ChatRoom = ({ username }) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // 1️⃣ Fetch chat history from backend when component mounts
    fetch("http://localhost:5000/chat/messages")
      .then((res) => res.json())
      .then((data) => setMessages(Array.isArray(data) ? data : []))
      .catch((err) => console.error("Error fetching chat history:", err));

    // 2️⃣ Join the chat room
    socket.emit("join", { username });

    // 3️⃣ Listen for new messages
    socket.on("receive_message", (data) => {
      setMessages((prev) => [...prev, data]);
    });

    // 4️⃣ Cleanup listener on unmount
    return () => socket.off("receive_message");
  }, [username]);

  // 5️⃣ Send message handler
  const sendMessage = (e) => {
    e.preventDefault();
    if (message.trim()) {
      // 🟢 FIX: Send 'content' instead of 'message'
      socket.emit("send_message", { username, content: message });
      setMessage("");
    }
  };

  return (
    <div className="chat-container">
      <h2>Welcome, {username}</h2>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.username}: </strong>
            {/* 🟢 FIX: Display msg.content instead of msg.message */}
            {msg.content}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatRoom;
