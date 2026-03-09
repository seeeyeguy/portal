import ApprovalsControls from "views/containers/AdminControls/ApprovalsControls/ApprovalsControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/approvals";

export default function AdminApprovals() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
      <main>
        <header>
          <h1>Approvals</h1>
        </header>
        <ApprovalsControls />
      </main>
    </AdminPanel>
  );
}
