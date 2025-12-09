import { render, screen, userEvent, within } from "test-utils";

import RecursiveAccordion from "views/components/RecursiveAccordion/RecursiveAccordion";

describe("`RecursiveAccordion` Tests", () => {
  test("Render `RecursiveAccordion`", () => {
    render(
      <RecursiveAccordion
        title="Engineering"
        dataSet={{
          "Hardware Engineering": [],
          "Project Engineering": [],
          "Software Engineering": [],
          "Systems Engineering": [],
        }}
        recursionDepth={0}
        isLoading={false}
        className=""
        AccordionHeaderContent={[<></>]}
      >
        {() => <></>}
      </RecursiveAccordion>
    );

    const element = screen.getByText(/^Engineering$/i);
    expect(element).toBeInTheDocument();
  });

  test("Open `RecursiveAccordion`", async () => {
    const user = userEvent.setup();
    render(
      <RecursiveAccordion
        title="Engineering"
        dataSet={{
          "Hardware Engineering": [],
          "Project Engineering": [],
          "Software Engineering": [],
          "Systems Engineering": [],
        }}
        recursionDepth={0}
        isLoading={false}
        className=""
        AccordionHeaderContent={[<></>]}
      >
        {() => <></>}
      </RecursiveAccordion>
    );

    const element = screen.getAllByRole("button");
    await user.click(element[0]);

    expect(
      within(element[0]).getByTestId("accordion-active")
    ).toBeInTheDocument();
  });
});
