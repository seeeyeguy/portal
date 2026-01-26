import { render, screen, userEvent, within } from "test-utils";

import FavoriteButton from "views/components/FavoriteButton/FavoriteButton";

describe("`FavoriteButton` Tests", () => {
  test("Render `FavoriteButton`", () => {
    render(
      <FavoriteButton
        isActive={false}
        disabled={false}
        className=""
        callback={() => undefined}
        errorCallback={() => undefined}
      />
    );

    const element = screen.getByRole("button");
    expect(element).toBeInTheDocument();

    expect(within(element).getByTestId("faStarThin-icon")).toBeInTheDocument();
  });

  test("Click `FavoriteButton`", async () => {
    const user = userEvent.setup();
    render(
      <FavoriteButton
        isActive={false}
        disabled={false}
        className=""
        callback={() => undefined}
        errorCallback={() => undefined}
      />
    );

    const element = screen.getByRole("button");
    expect(element).toBeInTheDocument();

    expect(within(element).getByTestId("faStarThin-icon")).toBeInTheDocument();

    await user.click(element);

    expect(within(element).getByTestId("faStar-icon")).toBeInTheDocument();
  });

  test("Render Disabled `FavoriteButton`", () => {
    render(
      <FavoriteButton
        isActive={false}
        disabled={true}
        className=""
        callback={() => undefined}
        errorCallback={() => undefined}
      />
    );

    const element = screen.getByRole("button");
    expect(element).toBeInTheDocument();

    expect(within(element).getByTestId("faStarThin-icon")).toBeInTheDocument();

    expect(element).toBeDisabled();
  });
});
