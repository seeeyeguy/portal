import React from "react";
import { Provider } from "react-redux";
import { ToastContainer } from "react-toastify";
import { cleanup, render, RenderOptions } from "@testing-library/react";
import { afterEach } from "vitest";

import store from "state/store";
import { toastContainerConfig } from "utils/packages/react-toastify";

afterEach(() => {
  cleanup();
});

// eslint-disable-next-line react-refresh/only-export-components
const AllProviders = ({ children }: { children: React.ReactNode }) => (
  <Provider store={store}>
    <ToastContainer {...toastContainerConfig} />
    {children}
  </Provider>
);

function customRender(
  component: React.ReactNode,
  options?: Omit<RenderOptions, "wrapper">
) {
  return render(component, {
    wrapper: AllProviders,
    ...options,
  });
}

// eslint-disable-next-line react-refresh/only-export-components
export * from "@testing-library/react";
export { default as userEvent } from "@testing-library/user-event";
export { customRender as render };
