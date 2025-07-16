import AccessControls from "views/containers/AdminControls/AccessControls/AccessControls";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminAccesses() {
  return (
    <AdminPanel path="/admin/accesses">
      <main>
        <header>
          <h1>Accesses</h1>
        </header>
        <AccessControls />
      </main>
    </AdminPanel>
  );
}
