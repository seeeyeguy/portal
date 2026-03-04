import Functions from "views/containers/AdminControls/Functions/Functions";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/functions";

export default function AdminFunctions() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Functions</h1>
          </header>
          <Functions />
        </main>
    </AdminPanel>
  );
}
