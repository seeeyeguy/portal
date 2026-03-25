import { createBrowserRouter, redirect } from "react-router-dom";

import RouteMenu from "views/containers/RouteMenu/RouteMenu";

import {
  AdminAccesses,
  AdminEmployeeLevels,
  AdminFunctions,
  AdminMaintenanceBanners,
  AdminReportingPeriod,
  AdminRequests,
  AdminRequestApprovals,
  AdminResources,
  AdminSubFunctions,
  AdminTags,
} from "views/pages/AdminPanel";
import Home from "views/pages/Home/Home";
import ProgramReviewTool from "views/pages/ProgramReviewTool/ProgramReviewTool";
import ProgramPerformance from "views/pages/ProgramPerformance/ProgramPerformance";

import { REDIRECT } from "definitions/StatusCodeConstants";
import { login } from "services/auth/ssoService";

import { IAuthUser } from "definitions/Sso.types";

export const ROUTES = [
  {
    path: "/",
    element: (
      <RouteMenu>
        <Home />
      </RouteMenu>
    ),
    loader: async () => {
      const user = (await login()) as Response | IAuthUser;
      if ("status" in user && user.status === REDIRECT) {
        return user;
      }
      return { user };
    },
  },
  {
    path: "/admin",
    children: [
      {
        index: true,
        element: (
          <RouteMenu>
            <AdminResources />
          </RouteMenu>
        ),
        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "accesses",
        element: (
          <RouteMenu>
            <AdminAccesses />
          </RouteMenu>
        ),

        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "employee-levels",
        element: (
          <RouteMenu>
            <AdminEmployeeLevels />
          </RouteMenu>
        ),

        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "functions",
        element: (
          <RouteMenu>
            <AdminFunctions />
          </RouteMenu>
        ),

        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "resources",
        loader: () => redirect("/admin"),
      },
      {
        path: "subfunctions",
        element: (
          <RouteMenu>
            <AdminSubFunctions />
          </RouteMenu>
        ),

        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "tags",
        element: (
          <RouteMenu>
            <AdminTags />
          </RouteMenu>
        ),

        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "reporting-period",
        element: (
          <RouteMenu>
            <AdminReportingPeriod />
          </RouteMenu>
        ),

        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "maintenance-banners",
        element: (
          <RouteMenu>
            <AdminMaintenanceBanners />
          </RouteMenu>
        ),

        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "requests",
        element: (
          <RouteMenu>
            <AdminRequests />
          </RouteMenu>
        ),
        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "request-approvals",
        element: (
          <RouteMenu>
            <AdminRequestApprovals />
          </RouteMenu>
        ),
        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
    ],
  },
  {
    path: "/prt",
    element: (
      <RouteMenu>
        <ProgramReviewTool />
      </RouteMenu>
    ),
    loader: async () => {
      const user = (await login()) as Response | IAuthUser;
      if ("status" in user && user.status === REDIRECT) {
        return user;
      }
      return { user };
    },
  },
  {
    path: "/ppr",
    element: (
      <RouteMenu>
        <ProgramPerformance />
      </RouteMenu>
    ),
    loader: async () => {
      const user = (await login()) as Response | IAuthUser;
      if ("status" in user && user.status === REDIRECT) {
        return user;
      }
      return { user };
    },
  },
  {
    path: "*",
    loader: () => redirect("/"),
  },
];

const router = createBrowserRouter(ROUTES);

export default router;
