import { render, screen, within } from "test-utils";

import ThumbnailLink from "views/components/ThumbnailLink/ThumbnailLink";

describe("`ThumbnailLink` Tests", () => {
  test("Render `ThumbnailLink`", () => {
    render(
      <ThumbnailLink
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
        maxLineHeight={2}
        leftOfLabelContent={null}
        rightOfLabelContent={null}
        callback={() => undefined}
      />
    );

    const element = screen.getByRole("link");
    expect(element).toBeInTheDocument();

    expect(
      within(element).getByAltText(/Web application/i)
    ).toBeInTheDocument();

    expect(
      within(element).getByText("Integrated Change Control")
    ).toBeInTheDocument();
  });
});
