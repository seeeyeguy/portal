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
    title: "Continue?",
    children: <></>,
    className: "",
    acceptLabel: <>Confirm</>,
    rejectLabel: <>Cancel</>,
    acceptClassName: "",
    rejectClassName: "",
    onHide: null,
  },
  render: (args) => {
    const [showModal, setShowModal] = React.useState(false);

    return (
      <>
        <ConfirmModal
          {...args}
          open={showModal}
          onAccept={() => {
            console.log("ACCEPTED");
            setShowModal(false);
          }}
          onReject={() => {
            console.log("REJECTED");
            setShowModal(false);
          }}
        />
        <button
          className="storybook-test-button"
          onClick={() => setShowModal(true)}
        >
          Open Modal
        </button>
      </>
    );
  },
};

export const OnlyAcceptCloses: Story = {
  args: {
    title: "Continue?",
    children: <></>,
    className: "",
    acceptLabel: <>Will Close</>,
    rejectLabel: <>Won't Close</>,
    acceptClassName: "",
    rejectClassName: "",
    onHide: null,
  },
  render: (args) => {
    const [showModal, setShowModal] = React.useState(false);

    return (
      <>
        <ConfirmModal
          {...args}
          open={showModal}
          onAccept={() => {
            console.log("ACCEPTED");
            setShowModal(false);
          }}
          onReject={() => {
            console.log("REJECTED");
          }}
        />
        <button
          className="storybook-test-button"
          onClick={() => setShowModal(true)}
        >
          Open Modal
        </button>
      </>
    );
  },
};

export const CustomStyle: Story = {
  args: {
    title: "Save Session",
    children: "Would you like to save your current session?",
    className: "test-modal-style",
    acceptLabel: <>Save</>,
    rejectLabel: <>Close</>,
    acceptClassName: "test-confirm-button",
    rejectClassName: "test-cancel-button",
  },
  render: (args) => {
    const [showModal, setShowModal] = React.useState(false);

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
        <ConfirmModal
          {...args}
          open={showModal}
          onAccept={() => {
            console.log("ACCEPTED");
            setShowModal(false);
          }}
          onReject={() => {
            console.log("REJECTED");
            setShowModal(false);
          }}
        />
        <button
          className="storybook-test-button"
          onClick={() => setShowModal(true)}
        >
          Open Modal
        </button>
      </>
    );
  },
};
