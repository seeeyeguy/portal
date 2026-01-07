import type { Meta, StoryObj } from "@storybook/react";

import FavoriteThumbnailLink from "views/components/FavoriteThumbnailLink/FavoriteThumbnailLink";

const meta = {
  title: "Links/FavoriteThumbnailLink",
  component: FavoriteThumbnailLink,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
    layout: "centered",
  },
} as Meta<typeof FavoriteThumbnailLink>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    name: "Integrated Change Control",
    description: "Integrated Change Control",
    url: "https://uspby1lnhdped05.gcsd.harris.com:2311/",
    thumbnail:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s",
    imgWidth: 95,
    imgHeight: 95,
    download: false,
    referrerPolicy: "strict-origin-when-cross-origin",
    rel: "",
    target: "_blank",
    className: "resource-link",
    showTooltip: true,
    tooltipPlace: "left-start",
    tooltipDelay: 1000,
    tooltipHTMLContent: (
      <a
        style={{ color: "#ffffff" }}
        href="mailto:michael.c.mullings@l3harris.com"
      >
        Contact Us
      </a>
    ),
    maxLineHeight: 1,
    isButtonActive: false,
    isButtonDisabled: false,
    buttonClassName: "",
    leftOfLabelContent: null,
    callback: () => undefined,
    buttonCallback: () => undefined,
    buttonErrorCallback: () => undefined,
  },
};

export const Contracts: Story = {
  args: {
    name: "Contracts",
    description: "Contracts Application",
    url: "https://uspby1lnhdped04.gcsd.harris.com:51500/rfp-review-memo/",
    thumbnail:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s",
    imgWidth: 95,
    imgHeight: 95,
    download: false,
    referrerPolicy: "strict-origin-when-cross-origin",
    rel: "",
    target: "_blank",
    className: "resource-link",
    showTooltip: true,
    tooltipPlace: "left-start",
    tooltipDelay: 1000,
    tooltipHTMLContent: (
      <a
        style={{ color: "#ffffff" }}
        href="mailto:michael.c.mullings@l3harris.com"
      >
        Contact Us
      </a>
    ),
    maxLineHeight: 1,
    isButtonActive: false,
    isButtonDisabled: false,
    buttonClassName: "",
    leftOfLabelContent: null,
    callback: () => undefined,
    buttonCallback: () => undefined,
    buttonErrorCallback: () => undefined,
  },
};

export const Tiering: Story = {
  args: {
    name: "Tiering",
    description: "Tiering Application",
    url: "https://usmlb1pmeo1p.rootforest.com/",
    thumbnail:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s",
    imgWidth: 95,
    imgHeight: 95,
    download: false,
    referrerPolicy: "strict-origin-when-cross-origin",
    rel: "",
    target: "_blank",
    className: "resource-link",
    showTooltip: true,
    tooltipPlace: "left-start",
    tooltipDelay: 1000,
    tooltipHTMLContent: (
      <a
        style={{ color: "#ffffff" }}
        href="mailto:michael.c.mullings@l3harris.com"
      >
        Contact Us
      </a>
    ),
    maxLineHeight: 1,
    isButtonActive: false,
    isButtonDisabled: false,
    buttonClassName: "",
    leftOfLabelContent: null,
    callback: () => undefined,
    buttonCallback: () => undefined,
    buttonErrorCallback: () => undefined,
  },
};

export const Dashboard: Story = {
  args: {
    name: "This Dashboard that has lots of cool features that are worth checking out",
    description: "A fancy Dashboard",
    url: "https://usmlb1pmeo1p.rootforest.com/",
    thumbnail:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s",
    imgWidth: 95,
    imgHeight: 95,
    download: false,
    referrerPolicy: "strict-origin-when-cross-origin",
    rel: "",
    target: "_blank",
    className: "resource-link",
    showTooltip: true,
    tooltipPlace: "left-start",
    tooltipDelay: 1000,
    tooltipHTMLContent: (
      <a
        style={{ color: "#ffffff" }}
        href="mailto:michael.c.mullings@l3harris.com"
      >
        Contact Us
      </a>
    ),
    maxLineHeight: 2,
    isButtonActive: false,
    isButtonDisabled: false,
    buttonClassName: "",
    leftOfLabelContent: null,
    callback: () => undefined,
    buttonCallback: () => undefined,
    buttonErrorCallback: () => undefined,
  },
};

export const IsFavoriteButtonDisabled: Story = {
  args: {
    name: "Integrated Change Control",
    description: "Integrated Change Control",
    url: "https://uspby1lnhdped05.gcsd.harris.com:2311/",
    thumbnail:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s",
    imgWidth: 95,
    imgHeight: 95,
    download: false,
    referrerPolicy: "strict-origin-when-cross-origin",
    rel: "",
    target: "_blank",
    className: "resource-link",
    showTooltip: true,
    tooltipPlace: "left-start",
    tooltipDelay: 1000,
    tooltipHTMLContent: (
      <a
        style={{ color: "#ffffff" }}
        href="mailto:michael.c.mullings@l3harris.com"
      >
        Contact Us
      </a>
    ),
    maxLineHeight: 1,
    isButtonActive: false,
    isButtonDisabled: true,
    buttonClassName: "",
    leftOfLabelContent: null,
    callback: () => undefined,
    buttonCallback: () => undefined,
    buttonErrorCallback: () => undefined,
  },
};
