import ResourceControls from "views/containers/AdminControls/ResourceControls/ResourceControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/resources";

export default function AdminResources() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Resources</h1>
          </header>
          <ResourceControls />
        </main>
    </AdminPanel>
  );
}
