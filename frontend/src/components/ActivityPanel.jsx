export default function ActivityPanel({ activities }) {
  return (
    <div className="activity-panel">
      <h2>Agent Activity</h2>

      {activities.length === 0 ? (
        <p className="muted">No tools called yet.</p>
      ) : (
        <div className="activity-list">
          {activities.map((activity, index) => (
            <div
              className="activity-card"
              key={`${activity.tool}-${index}`}
            >
              <div className="activity-title">
                ✓ {activity.tool}
              </div>

              <pre>
                {JSON.stringify(activity.arguments, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}