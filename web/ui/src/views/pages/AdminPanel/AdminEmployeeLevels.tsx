import EmployeeLevelsControls from "views/containers/AdminControls/EmployeeLevelControls/EmployeeLevelControls";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminEmployeeLevels() {
  return (
    <AdminPanel path="/admin/employee-levels">
      <main>
        <header>
          <h1>Employee Levels</h1>
        </header>
        <EmployeeLevelsControls />
      </main>
    </AdminPanel>
  );
}
