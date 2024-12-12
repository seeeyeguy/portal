import { createBrowserRouter, Navigate } from "react-router-dom";

import Home from "pages/Home";

import { REDIRECT } from "routes/api/helpers/headers/status-codes";
import { login } from "routes/pages/loaders/services/sso";

import { User } from "state/types/services/sso";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    loader: async () => {
      const user = (await login()) as Response | User;
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
