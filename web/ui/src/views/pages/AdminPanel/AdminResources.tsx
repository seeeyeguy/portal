import ResourceControls from "views/containers/AdminControls/ResourceControls/ResourceControls";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminResources() {
  return (
    <AdminPanel path="/admin/resources">
      <main>
        <header>
          <h1>Resources</h1>
        </header>
        <ResourceControls />
      </main>
    </AdminPanel>
  );
}
