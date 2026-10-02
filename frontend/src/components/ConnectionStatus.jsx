export default function ConnectionStatus({ status }) {
  const connected = status === "connected";

  return (
    <div className={`connection ${connected ? "connected" : "disconnected"}`}>
      <span className="dot" />
      {connected ? "WooCommerce connected" : "WooCommerce disconnected"}
    </div>
  );
}