import AccessControls from "views/containers/AdminControls/AccessControls/AccessControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/accesses";

export default function AdminAccesses() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Accesses</h1>
          </header>
          <AccessControls />
        </main>
    </AdminPanel>
  );
}
