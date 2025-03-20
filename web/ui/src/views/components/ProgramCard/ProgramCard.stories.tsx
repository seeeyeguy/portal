import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import ProgramCard from "views/components/ProgramCard/ProgramCard";

const meta: Meta<typeof ProgramCard> = {
  title: "ProgramCard/ProgramCard",
  component: ProgramCard,
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
      <ProgramCard
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
      id: 1,
      paNumber: "12HA",
      name: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractValue: 20500000,
      activeStatus: true,
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
      disabled: false,
    },
  },
  render: (args) => {
    return <ProgramCard {...args} />;
  },
};

export const IsInvalid: Story = {
  args: {
    program: {
      id: 1,
      paNumber: "12HA",
      name: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractValue: 20500000,
      activeStatus: false,
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
      disabled: false,
    },
  },
  render: (args) => {
    return <ProgramCard {...args} />;
  },
};

export const IsDisabled: Story = {
  args: {
    program: {
      id: 1,
      paNumber: "12HA",
      name: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractValue: 20500000,
      activeStatus: true,
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
      disabled: true,
    },
  },
  render: (args) => {
    return <ProgramCard {...args} />;
  },
};
