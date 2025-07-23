import ApprovalsControls from "views/containers/AdminControls/ApprovalsControls/ApprovalsControls";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminApprovals() {
  return (
    <AdminPanel path="/admin/approvals">
      <main>
        <header>
          <h1>Approvals</h1>
        </header>
        <ApprovalsControls />
      </main>
    </AdminPanel>
  );
}
