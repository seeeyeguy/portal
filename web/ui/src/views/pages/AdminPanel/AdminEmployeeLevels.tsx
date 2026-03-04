import EmployeeLevelsControls from "views/containers/AdminControls/EmployeeLevelControls/EmployeeLevelControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/employee-levels";

export default function AdminEmployeeLevels() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Employee Levels</h1>
          </header>
          <EmployeeLevelsControls />
        </main>
    </AdminPanel>
  );
}
