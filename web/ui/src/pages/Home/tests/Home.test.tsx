import { RouterProvider } from "react-router-dom";
import { render, screen, waitFor } from "test-utils";

import Home from "pages/Home";

import { login } from "routes/pages/loaders/services/sso";
import { createTestRouter } from "utils/tests/routers";

describe("`Home` Page Tests", () => {
  test("Render `Home` Page", async () => {
    const loader = async () => {
      const user = await login();
      return { user };
    };
    const router = createTestRouter("/", <Home />, loader, () => null);
    render(<RouterProvider router={router} />);
    await waitFor(() => screen.getByText("Hello, App!"));
    const element = screen.getByText("Hello, App!");
    expect(element).toBeInTheDocument();
  });
});
