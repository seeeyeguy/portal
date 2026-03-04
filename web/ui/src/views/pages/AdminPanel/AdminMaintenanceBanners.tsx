import MaintenanceBannerControls from "views/containers/AdminControls/MaintenanceBannersControls/MaintenanceBannerControls";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";

const path = "/admin/maintenance-banners";

export default function AdminMaintenanceBanners() {
  return (
    <AdminPanel path={path}>
      <MaintenanceBanner page={path} />
        <main>
          <header>
            <h1>Maintenance Banners</h1>
          </header>
          <MaintenanceBannerControls />
        </main>
    </AdminPanel>
  );
}
