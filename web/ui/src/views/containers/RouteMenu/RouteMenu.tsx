import React from "react";
import { useLoaderData, useNavigate } from "react-router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCalendarCheck,
  faChartLine,
  faCheckToSlot,
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
} from "@fortawesome/free-solid-svg-icons";
import lodash from "lodash";
import { MenuItem } from "primereact/menuitem";

import IconBadge from "views/components/IconBadge/IconBadge";
import SideBar, { IMenuLink } from "views/components/SideBar/SideBar";

import { IAuthUser } from "definitions/Sso.types";

import visitApi, {
  TApiPostVisitRequest,
} from "state/query/api/portal/analytics/AnalyticsApi";
import { useGetRequestsQuery } from "state/query/api/portal/request/RequestApi";
import { useAppDispatch } from "state/store/store";

import { requiredPermissions } from "utils/PermissionUtility";

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
  SMART_PERFORMANCE_METRICS: 132
  // TODO: Add PRT ID when resource is created in production.
};

const DRAFT_STAGE = 1;
const REVISE_STAGE = 4;

export default function RouteMenu({ children }: RouteMenuProps) {
  const loaderData = useLoaderData() as { user: IAuthUser };
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  // Get User `Request`s in the draft stage.
  const { data: requests } = useGetRequestsQuery({
    originator: loaderData.user.email,
    stages: [DRAFT_STAGE],
  });

  // Count number of `Request`s awaiting revision owned by user.
  const requestNotifications = React.useMemo(
    () =>
      requests?.data.reduce((count, request) => {
        const previousTransition =
          request.transitions.nodes[request.transitions.latest]
            .previousTransition;
        if (
          previousTransition &&
          request.transitions.nodes[previousTransition].stage.level ===
            REVISE_STAGE
        ) {
          return count + 1;
        }
        return count;
      }, 0) ?? 0,
    [requests]
  );


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

        // All permissions must be true for page to be visible.
        return {
          ...item,
          visible: requiredPermissions(loaderData.user, pathToCheck)
        };
      })
      .filter(
        // Remove menu items that are not visible.
        (item) =>
          item.visible ||
          item.items?.some((subItem: MenuItem) => subItem.visible)
      );
  }

  const onLinkClick = React.useCallback(async (id: number) => {
    const body: TApiPostVisitRequest = { resource: id };
    const promise = dispatch(visitApi.endpoints.addVisit.initiate(body));
    await promise;
  }, [dispatch]);

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
              "https://tableau.l3harris.com/#/workbooks/9049/views",
              "_blank",
              "noopener,noreferrer"
            );
          },
          icon: <FontAwesomeIcon icon={faChartLine} />,
          data: { path: "https://tableau.l3harris.com/#/workbooks/9049/views" },
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
          data: { path: "https://l3t.sharepoint.us/sites/Boots/Pub_Docs/Risk_Management.pdf" },
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
          badgeValue={requestNotifications > 0 ? " " : null}
          badgeClassName={styles["header-badge"]}
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
                requestNotifications > 0
                  ? requestNotifications?.toString()
                  : null
              }
            />
          ),
          data: { path: "/admin" },
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
          label: "Approvals",
          command: () => navigate("/admin/approvals"),
          icon: (
            <IconBadge
              icon={<FontAwesomeIcon icon={faCheckToSlot} />}
              badgeValue={null}
            />
          ),
          data: { path: "/admin/approvals" },
        },
        {
          label: "Accesses",
          command: () => navigate("/admin/accesses"),
          icon: <FontAwesomeIcon icon={faLock} />,
          data: { path: "/admin/accesses" },
        },
      ],
    },
  ];

  return (
    <>
      <SideBar
        header="Navigation"
        siblingId="page-content"
        menuLinks={processMenuItems(MENU_LINKS) as IMenuLink[]}
      />
      {children}
    </>
  );
}
