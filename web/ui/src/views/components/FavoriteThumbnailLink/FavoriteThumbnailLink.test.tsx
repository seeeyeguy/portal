import { render, screen, userEvent, within } from "test-utils";

import FavoriteThumbnailLink from "./FavoriteThumbnailLink";

describe("`FavoriteThumbnailLink` Tests", () => {
  test("Render `FavoriteThumbnailLink`", async () => {
    const user = userEvent.setup();
    render(
      <FavoriteThumbnailLink
        name="Integrated Change Control"
        description="Web application to store/manage changes in programs' baseline."
        url="https://uspby1lnhdped05.gcsd.harris.com:2311/"
        thumbnail="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s"
        imgWidth={95}
        imgHeight={95}
        download={false}
        referrerPolicy="strict-origin-when-cross-origin"
        rel=""
        target="_self"
        className=""
        showTooltip={true}
        tooltipPlace="left-start"
        tooltipDelay={1000}
        tooltipHTMLContent={<></>}
        maxLineHeight={1}
        isButtonActive={false}
        isButtonDisabled={false}
        buttonClassName=""
        leftOfLabelContent={null}
        callback={() => undefined}
        buttonCallback={() => undefined}
        buttonErrorCallback={() => undefined}
      />
    );

    const link = screen.getByRole("link");
    const button = screen.getByRole("button");
    expect(link).toBeInTheDocument();

    expect(button).toBeInTheDocument();

    expect(within(link).getByAltText(/Web application/i)).toBeInTheDocument();

    expect(
      within(link).getByText("Integrated Change Control")
    ).toBeInTheDocument();

    expect(within(button).getByTestId("faStarThin-icon")).toBeInTheDocument();

    await user.click(button);

    expect(within(button).getByTestId("faStar-icon")).toBeInTheDocument();
  });

  test("Render `FavoriteThumbnailLink` With Disabled `FavoriteButton`", async () => {
    render(
      <FavoriteThumbnailLink
        name="Integrated Change Control"
        description="Web application to store/manage changes in programs' baseline."
        url="https://uspby1lnhdped05.gcsd.harris.com:2311/"
        thumbnail="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s"
        imgWidth={95}
        imgHeight={95}
        download={false}
        referrerPolicy="strict-origin-when-cross-origin"
        rel=""
        target="_self"
        className=""
        showTooltip={true}
        tooltipPlace="left-start"
        tooltipDelay={1000}
        tooltipHTMLContent={<></>}
        maxLineHeight={1}
        isButtonActive={false}
        isButtonDisabled={true}
        buttonClassName=""
        leftOfLabelContent={null}
        callback={() => undefined}
        buttonCallback={() => undefined}
        buttonErrorCallback={() => undefined}
      />
    );

    const link = screen.getByRole("link");
    const button = screen.getByRole("button");
    expect(link).toBeInTheDocument();

    expect(button).toBeInTheDocument();

    expect(within(link).getByAltText(/Web application/i)).toBeInTheDocument();

    expect(
      within(link).getByText("Integrated Change Control")
    ).toBeInTheDocument();

    expect(within(button).getByTestId("faStarThin-icon")).toBeInTheDocument();

    expect(button).toBeDisabled();
  });
});
