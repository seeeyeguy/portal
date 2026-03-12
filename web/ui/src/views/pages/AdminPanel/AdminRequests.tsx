import RequestsControls from "views/containers/AdminControls/RequestsControls/RequestsControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/requests";

export default function AdminRequests() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
      <main>
        <header>
          <h1>Requests</h1>
        </header>
        <RequestsControls />
      </main>
    </AdminPanel>
  );
}