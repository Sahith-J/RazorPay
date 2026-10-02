import { useEffect, useState } from "react";

import { checkHealth } from "./api";
import ChatPanel from "./components/ChatPanel";
import ActivityPanel from "./components/ActivityPanel";
import ConnectionStatus from "./components/ConnectionStatus";

export default function App() {
  const [activities, setActivities] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState("checking");

  useEffect(() => {
    async function loadHealth() {
      try {
        const result = await checkHealth();

        setConnectionStatus(
          result.woocommerce === "connected"
            ? "connected"
            : "disconnected"
        );
      } catch {
        setConnectionStatus("disconnected");
      }
    }

    loadHealth();
  }, []);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>WooCommerce Support Agent</h1>
          <p>Razorpay Forward-Deployed Engineer Demo</p>
        </div>

        <ConnectionStatus status={connectionStatus} />
      </header>

      <main className="workspace">
        <ChatPanel onActivities={setActivities} />
        <ActivityPanel activities={activities} />
      </main>
    </div>
  );
}