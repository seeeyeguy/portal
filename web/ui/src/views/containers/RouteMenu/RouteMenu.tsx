import React from "react";
import { useLoaderData, useNavigate } from "react-router";
import { useGetProgramsQuery } from "state/query/api/portal/programReviewTool/ProgramApi";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCalendarCheck,
  faCalendarDay,
  faChartLine,
  faCheckToSlot,
  faFileLines,
  faFolder,
  faFolderTree,
  faHome,
  faLink,
  faListCheck,
  faLock,
  faMagnifyingGlassChart,
  faPersonChalkboard,
  faSitemap,
  faTag,
  faUserGear,
  faWrench,
} from "@fortawesome/free-solid-svg-icons";
import lodash from "lodash";
import { MenuItem } from "primereact/menuitem";

import IconBadge from "views/components/IconBadge/IconBadge";
import SideBar, { IMenuLink } from "views/components/SideBar/SideBar";

import { IAuthUser } from "definitions/Sso.types";

import visitApi, {
  TApiPostVisitRequest,
} from "state/query/api/portal/analytics/AnalyticsApi";
import { useSubscribeToRequestNotificationQuery } from "state/query/api/portal/request/RequestNotificationApi";
import { useAppDispatch } from "state/store/store";

import {
  hasBusinessProcessExpertPermissions,
  hasDataStewardPermissions,
  hasSuperuserPermissions,
  requiredPermissions,
} from "utils/PermissionUtility";

import styles from "views/containers/RouteMenu/RouteMenu.module.css";

function isMenuItem(item: MenuItem | IMenuLink): item is MenuItem {
  return !lodash.isNil((item as MenuItem).data);
}

function isIMenuLink(item: MenuItem | IMenuLink): item is IMenuLink {
  return !lodash.isNil((item as IMenuLink).path);
}

export interface RouteMenuProps {
  children: React.ReactNode;
}

// IDs of relevant Resource Links used in the sidebar for capturing visits.
const RESOURCE_LINKS = {
  PROGRAM_HEALTH_DASHBOARD: 59,
  RISK_TRACKER: 135,
  SMART_PERFORMANCE_METRICS: 132,
  // TODO: Add PRT ID when resource is created in production.
};

const REVISE_STAGE = 4;

const SUBMITTED = 2;
const APPROVED_BY_BPE = 3;

export default function RouteMenu({ children }: RouteMenuProps) {
  const loaderData = useLoaderData() as { user: IAuthUser };
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  //Check for programs that are active_status and tier 1 and 2
  const { data: programs } = useGetProgramsQuery({
    programMember: loaderData.user.email,
    tiers: [1, 2],
  });

  const hasPrograms = React.useMemo(
    () => Object.keys(programs?.data ?? {}).length > 0,
    [programs?.data]
  );

  const superuserPermissions = React.useMemo(
    () => hasSuperuserPermissions(loaderData.user),
    [loaderData]
  );

  const businessProcessExpertPermissions = React.useMemo(
    () => hasBusinessProcessExpertPermissions(loaderData.user),
    [loaderData]
  );

  const dataStewardPermissions = React.useMemo(
    () => hasDataStewardPermissions(loaderData.user),
    [loaderData]
  );

  const requestWS = useSubscribeToRequestNotificationQuery();

  const pendingRequests = React.useMemo(() => {
    if (dataStewardPermissions && requestWS?.data?.content) {
      return [...requestWS.data.content];
    }
    return [];
  }, [dataStewardPermissions, requestWS?.data]);

  const usersPermittedSubFunctions = React.useMemo(
    () =>
      Array.from(
        loaderData.user.accesses?.reduce((acc, access) => {
          access.subfunctions.forEach((id) => {
            if (!superuserPermissions) {
              acc.add(id);
            }
          });
          return acc;
        }, new Set<number>())
      ),
    [loaderData, superuserPermissions]
  );

  // Count number of `Request`s awaiting revision owned by user.
  const requestNotifications = React.useMemo(
    () =>
      pendingRequests.reduce((count, request) => {
        if (
          loaderData.user.username === request.originator &&
          request.stage === REVISE_STAGE
        ) {
          return count + 1;
        }
        return count;
      }, 0) ?? 0,
    [loaderData, pendingRequests]
  );

  // Memoized values for Superuser and Business Process Expert notifications.
  const [superuserNotifications, businessProcessExpertNotifications] =
    React.useMemo<[number, number]>(() => {
      const counts = pendingRequests.reduce(
        (acc, request) => {
          if (superuserPermissions && request.stage === APPROVED_BY_BPE) {
            acc.superuser += 1;
          }
          if (businessProcessExpertPermissions) {
            const hasMatchingSubFunctions = usersPermittedSubFunctions.some(
              (subfunction) => request.subfunctions.includes(subfunction)
            );
            if (hasMatchingSubFunctions && request.stage === SUBMITTED)
              acc.businessProcessExpert += 1;
          }

          return acc;
        },
        { superuser: 0, businessProcessExpert: 0 }
      ) ?? { superuser: 0, businessProcessExpert: 0 };

      // Only return notifications if user has the correct permissions.
      return [
        superuserPermissions ? counts.superuser : 0,
        businessProcessExpertPermissions ? counts.businessProcessExpert : 0,
      ];
    }, [
      businessProcessExpertPermissions,
      pendingRequests,
      superuserPermissions,
      usersPermittedSubFunctions,
    ]);

  function processMenuItems(
    items: MenuItem[] | IMenuLink[]
  ): MenuItem[] | IMenuLink[] {
    return items
      .map((item) => {
        if (item.items) {
          const filteredSubItems = processMenuItems(item.items as MenuItem[]);
          if (filteredSubItems.length > 0) {
            // Menu parent has children that are visible.
            return { ...item, items: filteredSubItems, visible: true };
          }

          // Menu parent has no visible children.
          return { ...item, items: filteredSubItems, visible: false };
        }

        let pathToCheck;

        if (isMenuItem(item)) {
          pathToCheck = item.data?.path;
        }

        if (isIMenuLink(item)) {
          pathToCheck = item.path;
        }

        if (item.label == "Program Performance (PPR)") {
          return {
            ...item,
            visible:
              requiredPermissions(loaderData.user, pathToCheck) && hasPrograms,
          };
        }

        // All permissions must be true for page to be visible.
        return {
          ...item,
          visible: requiredPermissions(loaderData.user, pathToCheck),
        };
      })
      .filter(
        // Remove menu items that are not visible.
        (item) =>
          item.visible ||
          item.items?.some((subItem: MenuItem) => subItem.visible)
      );
  }

  const onLinkClick = React.useCallback(
    async (id: number) => {
      const body: TApiPostVisitRequest = { resource: id };
      const promise = dispatch(visitApi.endpoints.addVisit.initiate(body));
      await promise;
    },
    [dispatch]
  );

  const MENU_LINKS: IMenuLink[] = [
    {
      label: "Home",
      command: () => navigate("/"),
      icon: <FontAwesomeIcon icon={faHome} />,
      path: "/",
    },
    {
      label: "Program Management Tools",
      icon: <FontAwesomeIcon icon={faListCheck} />,
      path: null,
      items: [
        {
          label: "Program Health Dashboard (PHD)",
          command: () => {
            onLinkClick(RESOURCE_LINKS.PROGRAM_HEALTH_DASHBOARD);
            window.open(
              "https://app.high.powerbigov.us/groups/me/apps/ac2afc6b-21b6-4e6f-8676-598620024698/reports/abc7a419-1eb8-4d3b-8512-901ecbf6f324/8581b61c07df049490e9",
              "_blank",
              "noopener,noreferrer"
            );
          },
          icon: <FontAwesomeIcon icon={faChartLine} />,
          data: { path: "https://tableau.l3harris.com/#/workbooks/9049/views" },
        },
        {
          label: "Program Performance (PPR)",
          command: () => navigate("/ppr"),
          icon: <FontAwesomeIcon icon={faFileLines} />,
          data: { path: "/ppr" },
        },
        {
          label: "Program Review Tool (PRT)",
          command: () => navigate("/prt"),
          icon: <FontAwesomeIcon icon={faPersonChalkboard} />,
          data: { path: "/prt" },
        },
        {
          label: "Risk Tracker",
          command: () => {
            onLinkClick(RESOURCE_LINKS.RISK_TRACKER);
            window.open(
              "https://l3t.sharepoint.us/sites/Boots/Pub_Docs/Risk_Management.pdf",
              "_blank",
              "noopener,noreferrer"
            );
          },
          icon: <FontAwesomeIcon icon={faMagnifyingGlassChart} />,
          data: {
            path: "https://l3t.sharepoint.us/sites/Boots/Pub_Docs/Risk_Management.pdf",
          },
        },
        {
          label: "SMART  ",
          command: () => {
            onLinkClick(RESOURCE_LINKS.SMART_PERFORMANCE_METRICS);
            window.open(
              "https://app.high.powerbigov.us/groups/me/apps/ac2afc6b-21b6-4e6f-8676-598620024698/reports/8aac33e4-11f2-49c8-b046-014e3ea95e7f/27ed44086901f988a701",
              "_blank",
              "noopener,noreferrer"
            );
          },
          icon: <FontAwesomeIcon icon={faCalendarCheck} />,
          data: { path: "https://tableau.l3harris.com/#/workbooks/9370/views" },
        },
      ],
    },
    {
      label: "Admin Pages",
      icon: (
        <IconBadge
          icon={<FontAwesomeIcon icon={faUserGear} />}
          badgeValue={
            requestNotifications ||
            businessProcessExpertNotifications ||
            superuserNotifications
              ? " "
              : null
          }
          badgeClassName={`${styles["header-badge"]} ${superuserNotifications ? styles["warning-badge"] : ""}`}
        />
      ),
      path: null,
      items: [
        {
          label: "Resources",
          command: () => navigate("/admin"),
          icon: (
            <IconBadge
              icon={<FontAwesomeIcon icon={faLink} />}
              badgeValue={
                requestNotifications ? requestNotifications?.toString() : null
              }
            />
          ),
          data: { path: "/admin" },
        },
        {
          label: "Requests",
          command: () => navigate("/admin/requests"),
          icon: <FontAwesomeIcon icon={faFileLines} />,
          data: { path: "/admin/requests" },
        },
        {
          label: "Request Approvals",
          command: () => navigate("/admin/request-approvals"),
          icon: (
            <IconBadge
              icon={<FontAwesomeIcon icon={faCheckToSlot} />}
              badgeValue={
                superuserNotifications + businessProcessExpertNotifications > 0
                  ? (
                      superuserNotifications +
                      businessProcessExpertNotifications
                    ).toString()
                  : null
              }
              badgeClassName={
                superuserNotifications ? styles["warning-badge"] : ""
              }
            />
          ),
          data: { path: "/admin/request-approvals" },
        },
        {
          label: "Employee Levels",
          command: () => navigate("/admin/employee-levels"),
          icon: <FontAwesomeIcon icon={faSitemap} />,
          data: { path: "/admin/employee-levels" },
        },
        {
          label: "Functions",
          command: () => navigate("/admin/functions"),
          icon: <FontAwesomeIcon icon={faFolder} />,
          data: { path: "/admin/functions" },
        },
        {
          label: "SubFunctions",
          command: () => navigate("/admin/subfunctions"),
          icon: <FontAwesomeIcon icon={faFolderTree} />,
          data: { path: "/admin/subfunctions" },
        },
        {
          label: "Tags",
          command: () => navigate("/admin/tags"),
          icon: <FontAwesomeIcon icon={faTag} />,
          data: { path: "/admin/tags" },
        },
        {
          label: "Accesses",
          command: () => navigate("/admin/accesses"),
          icon: <FontAwesomeIcon icon={faLock} />,
          data: { path: "/admin/accesses" },
        },
        {
          label: "Reporting Period",
          command: () => navigate("/admin/reporting-period"),
          icon: <FontAwesomeIcon icon={faCalendarDay} />,
          data: { path: "/admin/reporting-period" },
        },
        {
          label: "Maintenance Banners",
          command: () => navigate("/admin/maintenance-banners"),
          icon: <FontAwesomeIcon icon={faWrench} />,
          data: { path: "/admin/maintenance-banners" },
        },
      ],
    },
  ];

  return (
    <>
      <SideBar
        header="Navigation"
        menuLinks={processMenuItems(MENU_LINKS) as IMenuLink[]}
      />
      {children}
    </>
  );
}
