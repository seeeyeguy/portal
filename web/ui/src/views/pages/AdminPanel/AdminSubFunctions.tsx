import SubFunctions from "views/containers/AdminControls/SubFunctions/SubFunctions";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminSubFunctions() {
  return (
    <AdminPanel path="/admin/subfunctions">
      <main>
        <header>
          <h1>SubFunctions</h1>
        </header>
        <SubFunctions />
      </main>
    </AdminPanel>
  );
}
