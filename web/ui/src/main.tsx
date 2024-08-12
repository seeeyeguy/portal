import React from "react";
import ReactDOM from "react-dom/client";
import { Helmet, HelmetProvider } from "react-helmet-async";
import { Provider } from "react-redux";
import { RouterProvider } from "react-router";
import { ToastContainer } from "react-toastify";

import router from "routes/pages";
import store from "state/store";
import { toastContainerConfig } from "utils/packages/react-toastify";

import "react-toastify/dist/ReactToastify.css";
import "styles/global/root.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <HelmetProvider>
      <Helmet>
        <title>{__APP_NAME__}</title>
      </Helmet>
    </HelmetProvider>
    <Provider store={store}>
      <ToastContainer {...toastContainerConfig} />
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>
);
