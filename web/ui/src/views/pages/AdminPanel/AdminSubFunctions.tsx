import SubFunctions from "views/containers/AdminControls/SubFunctions/SubFunctions";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/subfunctions";

export default function AdminSubFunctions() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>SubFunctions</h1>
          </header>
          <SubFunctions />
        </main>
    </AdminPanel>
  );
}
