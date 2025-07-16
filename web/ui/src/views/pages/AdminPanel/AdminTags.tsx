
import TagControls from "views/containers/AdminControls/TagControls/TagControls";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminTags() {
  return (
    <AdminPanel path="/admin/tags">
      <main>
        <header>
          <h1>Tags</h1>
        </header>
        <TagControls/>
      </main>
    </AdminPanel>
  );
}
