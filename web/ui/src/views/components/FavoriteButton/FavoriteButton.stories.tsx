import type { Meta, StoryObj } from "@storybook/react";

import FavoriteButton from "views/components/FavoriteButton/FavoriteButton";

const meta = {
  title: "Buttons/FavoriteButton",
  component: FavoriteButton,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
    layout: "centered",
  },
} as Meta<typeof FavoriteButton>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    isActive: false,
    disabled: false,
    className: "",
    callback: () => undefined,
    errorCallback: () => undefined,
  },
};

export const IsDisabled: Story = {
  args: {
    isActive: false,
    disabled: true,
    className: "",
    callback: () => undefined,
    errorCallback: () => undefined,
  },
};
