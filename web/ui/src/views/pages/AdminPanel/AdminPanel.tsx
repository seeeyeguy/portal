import React from "react";
import { Navigate, useLoaderData } from "react-router";

import FAQModal from "views/components/FAQModal/FAQModal";
import NavBar from "views/components/NavBar/NavBar";

import { IProfile } from "definitions/portal/users/Profile.types";
import { IAuthUser } from "definitions/Sso.types";

import { useGetProfileUserQuery } from "state/query/api/portal/users/UsersApi";

import {
  hasNeededBusinessProcessExpertPermissions,
  hasNeededSuperuserPermissions,
} from "utils/PermissionUtility";

import styles from "views/pages/AdminPanel/AdminPanel.module.css";

export default function AdminPanel({
  path,
  children,
}: {
  path: string;
  children: React.ReactNode;
}) {
  const loaderData = useLoaderData() as { user: IAuthUser };

  // Refs to manipulate navbar profile menu.
  const smNavBarRef = React.useRef<HTMLElement>(null);
  const mdNavBarRef = React.useRef<HTMLElement>(null);
  const lgNavBarRef = React.useRef<HTMLElement>(null);

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

  const closeNavBarProfile = React.useCallback(() => {
    if (smNavBarRef.current) {
      smNavBarRef.current.click();
    }
    if (mdNavBarRef.current) {
      mdNavBarRef.current.click();
    }
    if (lgNavBarRef.current) {
      lgNavBarRef.current.click();
    }
  }, []);

  if (!loaderData.user.isAdmin && !loaderData.user.accesses?.length) {
    return <Navigate to="/" />;
  }

  if (!hasNeededSuperuserPermissions(loaderData.user, path)) {
    return <Navigate to="/admin" />;
  }

  if (!hasNeededBusinessProcessExpertPermissions(loaderData.user, path)) {
    return <Navigate to="/admin" />;
  }

  return (
    <div
      id="app-container"
      onClick={() => {
        closeNavBarProfile();
      }}
      aria-description="container for admin application"
    >
      <FAQModal />
      <NavBar
        profile={profile}
        hideSearchBar={true}
        navBarRefs={[smNavBarRef, mdNavBarRef, lgNavBarRef]}
      />
      <div
        id="page-content"
        className={`${styles["admin-content"]}`}
        aria-description="admin page content"
      >
        {children}
      </div>
    </div>
  );
}
