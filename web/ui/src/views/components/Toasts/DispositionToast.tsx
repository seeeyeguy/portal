interface DispositionToastProps {
  resource: string;
  action: string;
  user: string;
  cacheTimeout: number;
}

export function DispositionToast({
  resource,
  action,
  user,
  cacheTimeout
}: DispositionToastProps) {
  return (
    <div>
      <h3 style={{ margin: 0, fontWeight: 600 }}>Resource Updated</h3>

      <div style={{ whiteSpace: "pre-line", marginTop: "8px" }}>
        {resource} <strong>{action}</strong> by {user}
        {`\n\nIt may take up to ${cacheTimeout} minutes for the update to appear.`}
      </div>
    </div>
  );
}
