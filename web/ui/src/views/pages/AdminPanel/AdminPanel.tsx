import React from "react";
import { Navigate, useLoaderData, useNavigate } from "react-router";
import {
  faCheckToSlot,
  faLink,
  faLock,
  faSitemap,
  faTag,
  faUserGear,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { MenuItem } from "primereact/menuitem";

import FAQModal from "views/components/FAQModal/FAQModal";
import NavBar from "views/components/NavBar/NavBar";
import SideBar from "views/components/SideBar/SideBar";

import { IProfile } from "definitions/portal/users/Profile.types";
import { IAuthUser } from "definitions/Sso.types";

import { useGetProfileUserQuery } from "state/query/api/portal/users/UsersApi";

import styles from "views/pages/AdminPanel/AdminPanel.module.css";

const ROLE_LEVELS = {
  SUPERUSER: 1,
  BUSINESS_PROCESS_EXPERT: 2,
};

const RESTRICTED_ADMIN_PAGES = {
  SUPERUSER: new Set([
    "/admin/accesses",
    "/admin/employee-levels",
    "/admin/functions",
    "/admin/subfunctions",
  ]),
  BUSINESS_PROCESS_EXPERT: new Set(["/admin/approvals"]),
};

export default function AdminPanel({
  path,
  children,
}: {
  path: string;
  children: React.ReactNode;
}) {
  const loaderData = useLoaderData() as { user: IAuthUser };
  const navigate = useNavigate();

  const hasNeededSuperuserPermissions = React.useCallback(
    (urlPath: string) => {
      if (!RESTRICTED_ADMIN_PAGES.SUPERUSER.has(urlPath)) {
        return true;
      }
      return (
        loaderData.user.accesses?.some(
          (access) => access.role.level == ROLE_LEVELS.SUPERUSER
        ) || loaderData.user.isAdmin
      );
    },
    [loaderData]
  );

  const hasNeededBusinessProcessExpertPermissions = React.useCallback(
    (urlPath: string) => {
      if (!RESTRICTED_ADMIN_PAGES.BUSINESS_PROCESS_EXPERT.has(urlPath)) {
        return true;
      }

      return (
        loaderData.user.accesses?.some(
          (access) =>
            access.role.level == ROLE_LEVELS.SUPERUSER ||
            access.role.level == ROLE_LEVELS.BUSINESS_PROCESS_EXPERT
        ) || loaderData.user.isAdmin
      );
    },
    [loaderData]
  );

  const sideBarMenuItems = React.useMemo(() => {
    const baseItems = [
      {
        label: "Resources",
        command: () => navigate("/admin/resources"),
        icon: <FontAwesomeIcon icon={faLink} />,
        path: "/admin/resources",
      },
      {
        label: "Employee Levels",
        command: () => navigate("/admin/employee-levels"),
        icon: <FontAwesomeIcon icon={faSitemap} />,
        path: "/admin/employee-levels",
      },
      {
        label: "Functions",
        command: () => navigate("/admin/functions"),
        icon: <FontAwesomeIcon icon={faSitemap} />,
        path: "/admin/functions",
      },
      {
        label: "SubFunctions",
        command: () => navigate("/admin/subfunctions"),
        icon: <FontAwesomeIcon icon={faSitemap} />,
        path: "/admin/subfunctions",
      },
      {
        label: "Tags",
        command: () => navigate("/admin/tags"),
        icon: <FontAwesomeIcon icon={faTag} />,
        path: "/admin/tags",
      },
      {
        label: "Approvals",
        command: () => navigate("/admin/approvals"),
        icon: <FontAwesomeIcon icon={faCheckToSlot} />,
        path: "/admin/approvals",
      },
      {
        label: "Accesses",
        command: () => navigate("/admin/accesses"),
        icon: <FontAwesomeIcon icon={faLock} />,
        path: "/admin/accesses",
      },
    ];
    return baseItems.reduce((acc, item) => {
      if (
        !hasNeededSuperuserPermissions(item.path) ||
        !hasNeededBusinessProcessExpertPermissions(item.path)
      ) {
        return acc;
      }

      return [...acc, item];
    }, [] as MenuItem[]);
  }, [
    hasNeededBusinessProcessExpertPermissions,
    hasNeededSuperuserPermissions,
    navigate,
  ]);

  const { data: profileApiResponse } = useGetProfileUserQuery(
    loaderData.user.email
  );

  const profile = (profileApiResponse?.data ?? {
    user: {
      firstName: loaderData.user.firstName,
      lastName: loaderData.user.lastName,
      email: loaderData.user.email,
    },
    jobTitle: "UNKNOWN",
    citizenship: "UNKNOWN",
  }) as IProfile;

  if (!loaderData.user.isAdmin && !loaderData.user.accesses?.length) {
    return <Navigate to="/" />;
  }

  if (!hasNeededSuperuserPermissions(path)) {
    return <Navigate to="/admin" />;
  }

  if (!hasNeededBusinessProcessExpertPermissions(path)) {
    return <Navigate to="/admin" />;
  }

  return (
    <>
      <FAQModal />
      <NavBar profile={profile} hideSearchBar={true} />
      <SideBar
        header="Navigation"
        menuLinks={[
          {
            label: "Admin Pages",
            icon: <FontAwesomeIcon icon={faUserGear} />,
            items: sideBarMenuItems,
          },
        ]}
        siblingId="page-content"
      />
      <div
        id="page-content"
        className={`${styles["admin-content"]}`}
        aria-description="admin page content"
      >
        {children}
      </div>
    </>
  );
}
