import ReportingPeriodControls from "views/containers/AdminControls/ReportingPeriodControls/ReportingPeriodControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/reporting-period";

export default function AdminReportingPeriod() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Reporting Period Administration</h1>
          </header>
          <ReportingPeriodControls />
        </main>
    </AdminPanel>
  );
}
