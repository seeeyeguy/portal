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
      id: 1,
      paNumber: "12HA",
      name: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractType: "FFP",
      contractNumber: "CN451452",
      contractValue: 20500000,
      contractStartDate: "2025-01-01",
      contractEndDate: "2025-12-01",
      actualCostWorkPerformedCumulative: 70.36,
      budgetedCostWorkPerformedCumulative: 20.55,
      budgetedCostWorkScheduledCumulative: 59.46,
      costPerformanceIndexCumulative: 0.61,
      schedulePerformanceIndexCumulative: 0.55,
      budgetAtComplete: 41.97,
      estimateAtComplete: 84.95,
      estimateToComplete: 36.02,
      managementReserve: 47.9,
      weightedRisksAndOpportunities: 30.27,
      activeStatus: true,
      teamMembers: [],
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
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
      id: 1,
      paNumber: "12HA",
      name: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractType: "FFP",
      contractNumber: "CN451452",
      contractValue: 20500000,
      contractStartDate: "2025-01-01",
      contractEndDate: "2025-12-01",
      actualCostWorkPerformedCumulative: 70.36,
      budgetedCostWorkPerformedCumulative: 20.55,
      budgetedCostWorkScheduledCumulative: 59.46,
      costPerformanceIndexCumulative: 0.61,
      schedulePerformanceIndexCumulative: 0.55,
      budgetAtComplete: 41.97,
      estimateAtComplete: 84.95,
      estimateToComplete: 36.02,
      managementReserve: 47.9,
      weightedRisksAndOpportunities: 30.27,
      activeStatus: false,
      teamMembers: [],
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
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
      id: 1,
      paNumber: "12HA",
      name: "Program 12HA",
      sector: "Sector Awesome",
      division: "Division Amazing",
      tier: 2,
      contractType: "FFP",
      contractNumber: "CN451452",
      contractValue: 20500000,
      contractStartDate: "2025-01-01",
      contractEndDate: "2025-12-01",
      actualCostWorkPerformedCumulative: 70.36,
      budgetedCostWorkPerformedCumulative: 20.55,
      budgetedCostWorkScheduledCumulative: 59.46,
      costPerformanceIndexCumulative: 0.61,
      schedulePerformanceIndexCumulative: 0.55,
      budgetAtComplete: 41.97,
      estimateAtComplete: 84.95,
      estimateToComplete: 36.02,
      managementReserve: 47.9,
      weightedRisksAndOpportunities: 30.27,
      activeStatus: true,
      teamMembers: [],
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
      disabled: true,
    },
  },
  render: (args) => {
    return <ProgramCardCondensed {...args} />;
  },
};
