import { createBrowserRouter, Navigate } from "react-router-dom";

import {
  AdminAccesses,
  AdminApprovals,
  AdminEmployeeLevels,
  AdminFunctions,
  AdminResources,
  AdminSubFunctions,
  AdminTags,
} from "views/pages/AdminPanel";
import Home from "views/pages/Home/Home";
import ProgramReviewTool from "views/pages/ProgramReviewTool/ProgramReviewTool";

import { REDIRECT } from "definitions/StatusCodeConstants";
import { login } from "services/auth/ssoService";

import { IAuthUser } from "definitions/Sso.types";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
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
        element: <AdminResources />,
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
        element: <AdminAccesses />,
        loader: async () => {
          const user = (await login()) as Response | IAuthUser;
          if ("status" in user && user.status === REDIRECT) {
            return user;
          }
          return { user };
        },
      },
      {
        path: "approvals",
        element: <AdminApprovals />,
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
        element: <AdminEmployeeLevels />,
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
        element: <AdminFunctions />,
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
        element: <Navigate to="/admin" />,
      },
      {
        path: "subfunctions",
        element: <AdminSubFunctions />,
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
        element: <AdminTags />,
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
    element: <ProgramReviewTool />,
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
    element: <Navigate to="/" />,
  },
]);

export default router;
