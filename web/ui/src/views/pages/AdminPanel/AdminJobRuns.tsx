import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import { Dropdown, DropdownChangeEvent } from "primereact/dropdown";
import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";


const path = "/admin/job-runs";

export default function AdminJobRuns() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Server Jobs</h1>
          </header>
        </main>
    </AdminPanel>
  );

