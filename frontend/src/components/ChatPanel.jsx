import { useState } from "react";
import { sendChatMessage } from "../api";

export default function ChatPanel({ onActivities }) {
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "agent",
      text: "Ask me about WooCommerce orders, products, or inventory.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmed = message.trim();

    if (!trimmed || loading) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        role: "user",
        text: trimmed,
      },
    ]);

    setMessage("");
    setLoading(true);
    onActivities([]);

    try {
      const result = await sendChatMessage(trimmed);

      setMessages((current) => [
        ...current,
        {
          role: "agent",
          text: result.answer,
        },
      ]);

      onActivities(result.activities || []);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "agent",
          text: `Error: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-panel">
      <div className="messages">
        {messages.map((item, index) => (
          <div
            key={index}
            className={`message ${item.role}`}
          >
            <div className="message-role">
              {item.role === "user" ? "You" : "Agent"}
            </div>

            <div className="message-content">
              {item.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message agent">
            <div className="message-role">
              Agent
            </div>

            <div className="message-content">
              Working...
            </div>
          </div>
        )}
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask about an order, product, or inventory..."
        />

        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
}