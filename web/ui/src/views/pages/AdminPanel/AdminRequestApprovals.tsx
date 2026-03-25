import RequestApprovalsControls from "views/containers/AdminControls/RequestApprovalsControls/RequestApprovalsControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/request-approvals";

export default function AdminRequests() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
      <main>
        <header>
          <h1>Request Approvals</h1>
        </header>
        <RequestApprovalsControls />
      </main>
    </AdminPanel>
  );
}
