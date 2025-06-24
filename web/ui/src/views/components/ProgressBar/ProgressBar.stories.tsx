import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import ProgressBar, {
  IProgressMarker,
} from "views/components/ProgressBar/ProgressBar";

const meta: Meta<typeof ProgressBar> = {
  title: "ProgressBar",
  component: ProgressBar,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "step 1", complete: true },
      { id: 2, name: "step 2", complete: false },
      { id: 3, name: "step 3", complete: false },
      { id: 4, name: "step 4", complete: false },
    ],
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const DiscreteEmpty: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: false },
      { id: 2, name: "Step 2", complete: false },
      { id: 3, name: "Step 3", complete: false },
      { id: 4, name: "Step 4", complete: false },
    ],
    discreteUnit: "Steps",
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const Discrete: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: true },
      { id: 2, name: "Step 2", complete: true },
      { id: 3, name: "Step 3", complete: false },
      { id: 4, name: "Step 4", complete: false },
    ],
    discreteUnit: "Steps",
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const DiscreteWithIncompleteMarker: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: true },
      { id: 2, name: "Step 2", complete: true },
      { id: 3, name: "Step 3", complete: false },
      { id: 4, name: "Step 4", complete: false },
    ],
    discreteUnit: "Steps",
    currentMarker: 3,
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const DiscreteWithCompleteMarker: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: true },
      { id: 2, name: "Step 2", complete: true },
      { id: 3, name: "Step 3", complete: true },
      { id: 4, name: "Step 4", complete: false },
    ],
    discreteUnit: "Steps",
    currentMarker: 3,
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const DiscreteCentered: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: true },
      { id: 2, name: "Step 2", complete: true },
      { id: 3, name: "Step 3", complete: false },
      { id: 4, name: "Step 4", complete: false },
    ],
    discreteUnit: "Steps",
    currentMarker: 3,
    centeredLabel: true,
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const NoDisplayedValue: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: true },
      { id: 2, name: "Step 2", complete: true },
      { id: 3, name: "Step 3", complete: true },
      { id: 4, name: "Step 4", complete: false },
    ],
    showValue: false,
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const Striped: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: true },
      { id: 2, name: "Step 2", complete: true },
      { id: 3, name: "Step 3", complete: true },
      { id: 4, name: "Step 4", complete: false },
    ],
    showValue: false,
    striped: true,
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const AlternateColors: Story = {
  args: {
    progressMarkers: [
      { id: 1, name: "Step 1", complete: true },
      { id: 2, name: "Step 2", complete: true },
      { id: 3, name: "Step 3", complete: true },
      { id: 4, name: "Step 4", complete: true },
    ],
    showValue: true,
    striped: true,
    discreteUnit: "Steps",
    progressColor: "#ded52a",
    progressLabelColor: "#000",
  },
  render: (args) => {
    return <ProgressBar {...args} />;
  },
};

export const ActiveExample: Story = {
  args: {
    showValue: true,
    discreteUnit: "",
    striped: true,
    totalCompletionLabel: "Request Completed",
    markerCompleteLabel: "Finalized",
    markerIncompleteLabel: "Staged",
    progressColor: "#35b939",
  },
  render: (args) => {
    const initalProgressMarkers: IProgressMarker[] = React.useMemo(
      () => [
        {
          id: 1,
          name: "Submission",
          complete: false,
          completeLabel: "Submitted",
        },
        { id: 2, name: "Processing", complete: false },
        {
          id: 3,
          name: "Approval",
          complete: false,
          incompleteLabel: "Awaiting Authorization",
        },
        { id: 4, name: "Finalization", complete: false },
      ],
      []
    );

    const [currentMarker, setCurrentMarker] = React.useState(
      initalProgressMarkers[0].id
    );
    const [progressMarkers, setProgressMarkers] = React.useState(
      initalProgressMarkers
    );

    /* Loops over progress markers and changes marker state
     * and the current marker for demonstration purposes.
     */
    React.useEffect(() => {
      const timer = setInterval(() => {
        const tempMarker = progressMarkers.find(
          (marker) => marker.id === currentMarker
        );

        if (!tempMarker) {
          setProgressMarkers(initalProgressMarkers);
          setCurrentMarker(initalProgressMarkers[0].id);
          return;
        }

        if (!tempMarker?.complete) {
          setProgressMarkers((prevMarkers) =>
            prevMarkers.map((marker) =>
              marker.id === tempMarker?.id
                ? { ...marker, complete: true }
                : marker
            )
          );
        } else {
          setCurrentMarker(currentMarker + 1);
        }
      }, 3000);

      return () => clearInterval(timer);
    }, [progressMarkers, currentMarker, initalProgressMarkers]);

    return (
      <ProgressBar
        {...args}
        currentMarker={currentMarker}
        progressMarkers={progressMarkers}
      />
    );
  },
};
