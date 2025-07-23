import type { Meta, StoryObj } from "@storybook/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlusSquare } from "@fortawesome/free-solid-svg-icons";

import IconBadge from "views/components/IconBadge/IconBadge";

import styles from "views/components/IconBadge/IconBadge.stories.module.css";

const meta: Meta<typeof IconBadge> = {
  title: "IconBadge",
  component: IconBadge,
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
    icon: <FontAwesomeIcon icon={faPlusSquare} size={"2xl"} />,
  },
  render: (args) => {
    return <IconBadge {...args} />;
  },
};

export const NoBadge: Story = {
  args: {
    icon: <FontAwesomeIcon icon={faPlusSquare} size={"2xl"} />,
    badgeValue: null,
  },
  render: (args) => {
    return <IconBadge {...args} />;
  },
};

export const BadgeStyled: Story = {
  args: {
    icon: <FontAwesomeIcon icon={faPlusSquare} size={"2xl"} />,
    badgeValue: "5",
    badgeClassName: styles["custom-badge"],
  },
  render: (args) => {
    return <IconBadge {...args} />;
  },
};
