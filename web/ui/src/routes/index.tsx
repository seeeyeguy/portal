import { createBrowserRouter, Navigate } from "react-router-dom";

import Home from "views/pages/Home/Home";
import ProgramReviewTool from "views/pages/ProgramReviewTool/ProgramReviewTool";

import { REDIRECT } from "definitions/StatusCodeConstants";
import { login } from "services/auth/ssoService";

import { IUser } from "definitions/Sso.types";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    loader: async () => {
      const user = (await login()) as Response | IUser;
      if ("status" in user && user.status === REDIRECT) {
        return user;
      }
      return { user };
    },
  },
  {
    path: "/prt",
    element: <ProgramReviewTool />,
    loader: async () => {
      const user = (await login()) as Response | IUser;
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
