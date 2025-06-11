import React from "react";
import ReactDOM from "react-dom/client";
import { Helmet, HelmetProvider } from "react-helmet-async";
import { Provider } from "react-redux";
import { RouterProvider } from "react-router";
import { ToastContainer } from "react-toastify";

import router from "routes";
import store from "state/store/store";
import { toastContainerConfig } from "definitions/ReactToastifyConstants";

import "react-toastify/dist/ReactToastify.css";
import "views/styles/global/colors.css";
import "views/styles/global/root.css";
import "views/styles/global/zIndex.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <HelmetProvider>
      <Helmet>
        <title>{__APP_TITLE__}</title>
        <meta
          property="og:url"
          content={`${__SCHEME__}://${__WEB_HOST__}:${__WEB_PORT__}`}
        />
        <meta property="og:title" content={__APP_NAME__} />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content={__APP_NAME__} />
        <meta
          property="og:description"
          content="A directory of helpful services and resources."
        />
        <meta
          property="og:image"
          content={`${__SCHEME__}://${__WEB_HOST__}:${__WEB_PORT__}/icon/portal-logo.png`}
        />
      </Helmet>
    </HelmetProvider>
    <Provider store={store}>
      <ToastContainer {...toastContainerConfig} />
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>
);
