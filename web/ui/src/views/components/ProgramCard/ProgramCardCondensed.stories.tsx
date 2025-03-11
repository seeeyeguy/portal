import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import ProgramCardCondensed from "views/components/ProgramCard/ProgramCardCondensed";

const meta: Meta<typeof ProgramCardCondensed> = {
  title: "ProgramCard/ProgramCardCondensed",
  component: ProgramCardCondensed,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
  render: (args) => {
    const [inputValue, setInputValue] = React.useState("");

    return (
      <ProgramCardCondensed
        {...args}
        inputValue={inputValue}
        setInputValue={setInputValue}
      />
    );
  },
};

export const IsValid: Story = {
  args: {
    program: {
      id: "1",
      paNumber: "12HA",
      programName: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractValue: "20.5M",
      valid: true,
      disabled: false,
    },
  },
  render: (args) => {
    return <ProgramCardCondensed {...args} />;
  },
};

export const IsInvalid: Story = {
  args: {
    program: {
      id: "1",
      paNumber: "12HA",
      programName: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractValue: "20.5M",
      valid: false,
      disabled: false,
    },
  },
  render: (args) => {
    return <ProgramCardCondensed {...args} />;
  },
};

export const IsDisabled: Story = {
  args: {
    program: {
      id: "1",
      paNumber: "12HA",
      programName: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractValue: "20.5M",
      valid: true,
      disabled: true,
    },
  },
  render: (args) => {
    return <ProgramCardCondensed {...args} />;
  },
};
