import { createMemoryRouter } from "react-router-dom";
import type { ActionFunction, LoaderFunction } from "react-router-dom";

export function createTestRouter(
  path: string,
  element: React.ReactNode,
  loader: LoaderFunction,
  action: ActionFunction
) {
  const routes = [
    {
      path,
      element,
      loader,
      action,
    },
  ];
  const router = createMemoryRouter(routes, {
    initialEntries: ["/"],
    initialIndex: 1,
  });
  return router;
}
