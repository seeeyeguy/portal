import MaintenanceBannerControls from "views/containers/AdminControls/MaintenanceBannersControls/MaintenanceBannerControls";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

export default function AdminMaintenanceBanners() {
  return (
    <AdminPanel path="/admin/maintenance-banners">
      <main>
        <header>
          <h1>Maintenance Banners</h1>
        </header>
        <MaintenanceBannerControls />
      </main>
    </AdminPanel>
  );
}