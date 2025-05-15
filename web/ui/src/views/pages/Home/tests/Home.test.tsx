import { RouterProvider } from "react-router-dom";
import { render, screen, waitFor } from "tests/test-utils";

import Home from "views/pages/Home/Home";

import { login } from "services/auth/ssoService";
import { createTestRouter } from "tests/routers";

describe("`Home` Page Tests", () => {
  beforeEach(() => {
    HTMLDialogElement.prototype.showModal = vitest.fn();
    HTMLDialogElement.prototype.close = vitest.fn();
  });

  test("Render `Home` Page", async () => {
    const loader = async () => {
      const user = await login();
      return { user };
    };
    const router = createTestRouter("/", <Home />, loader, () => null);
    render(<RouterProvider router={router} />);
    await waitFor(() => screen.getByText("Function"));
    const element = screen.getByText("Function");
    expect(element).toBeInTheDocument();
  });
});
