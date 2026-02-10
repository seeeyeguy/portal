import ReportingPeriodControls from "views/containers/AdminControls/ReportingPeriodControls/ReportingPeriodControls";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminReportingPeriod() {
  return (
    <AdminPanel path="/admin/reporting-period">
      <main>
        <header>
          <h1>Reporting Period Administration</h1>
        </header>
        <ReportingPeriodControls />
      </main>
    </AdminPanel>
  );
}
