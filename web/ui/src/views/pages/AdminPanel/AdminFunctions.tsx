import Functions from "views/containers/AdminControls/Functions/Functions";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminFunctions() {
  return (
    <AdminPanel path="/admin/functions">
      <main>
        <header>
          <h1>Functions</h1>
        </header>
        <Functions />
      </main>
    </AdminPanel>
  );
}
