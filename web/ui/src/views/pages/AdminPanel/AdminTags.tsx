import TagControls from "views/containers/AdminControls/TagControls/TagControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/tags";

export default function AdminTags() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Tags</h1>
          </header>
          <TagControls />
        </main>
    </AdminPanel>
  );
}
