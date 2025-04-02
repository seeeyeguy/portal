import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";

const meta: Meta<typeof ConfirmModal> = {
  title: "ConfirmModal",
  component: ConfirmModal,
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
    open: true,
    title: "Continue?",
    children: <></>,
    className: "",
    acceptLabel: <>Confirm</>,
    rejectLabel: <>Cancel</>,
    acceptClassName: "",
    rejectClassName: "",
    onAccept: () => console.log("ACCEPTED"),
    onReject: () => console.log("REJECTED"),
    onHide: undefined,
  },
  render: (args) => {
    return <ConfirmModal {...args} />;
  },
};

export const CustomStyle: Story = {
  args: {
    open: true,
    title: "Save Session",
    children: "Would you like to save your current session?",
    className: "test-modal-style",
    acceptLabel: <>Save</>,
    rejectLabel: <>Close</>,
    acceptClassName: "test-confirm-button",
    rejectClassName: "test-cancel-button",
    onAccept: () => console.log("SAVED"),
    onReject: () => console.log("CLOSED"),
    onHide: () => console.log("HIDDEN"),
  },
  render: (args) => {
    return (
      <>
        <style>
          {`
        .test-modal-style {
          background: var(--color-stealth);
          color: var(--color-white);
        }

        .test-modal-style header {
          background: var(--color-stealth);
          color: var(--color-white);
        }

        .test-confirm-button {
          background: var(--color-white);
          font-weight: bold;
        }

        .test-cancel-button {
          background: var(--color-white);
          font-weight: bold;
        }
      `}
        </style>
        <ConfirmModal {...args} />
      </>
    );
  },
};
