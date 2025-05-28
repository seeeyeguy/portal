import type { Meta, StoryObj } from "@storybook/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCalendarDays,
  faChartLine,
  faChartSimple,
  faCirclePlus,
  faDatabase,
  faDashboard,
  faListCheck,
  faSquareCheck,
  faTriangleExclamation,
} from "@fortawesome/free-solid-svg-icons";

import SideBar, { IMenuLink } from "views/components/SideBar/SideBar";

const MENU_LINKS: IMenuLink[] = [
  {
    label: "Administration",
    icon: <FontAwesomeIcon icon={faListCheck} />,
    items: [
      {
        label: "Add Resource",
        command: () => console.log("TEST"),
        icon: <FontAwesomeIcon icon={faCirclePlus} />,
      },
      {
        label: "Approve Request",
        command: () => console.log("TEST"),
        icon: <FontAwesomeIcon icon={faSquareCheck} />,
      },
    ],
    customContent: (
      <div
        aria-description="test links"
        style={{ display: "flex", flexDirection: "column", flex: 1 }}
      >
        <a href="url">How to approve a resource?</a>
        <a href="url">Where to get permissions?</a>
        <a href="url">Who is my admin?</a>
        <hr></hr>
        <a href="url">My Links</a>
        <a href="url">My Tools</a>
        <a href="url">My Favorites</a>
        <hr></hr>
        <a href="url">My Links</a>
        <a href="url">My Tools</a>
        <a href="url">My Favorites</a>
      </div>
    ),
  },
  {
    label: "Program",
    icon: <FontAwesomeIcon icon={faChartLine} />,
    items: [
      {
        label: "Program Review",
        items: [
          {
            label: "PRT",
            url: "/?path=/docs/programcard-programcard--docs",
            icon: <FontAwesomeIcon icon={faCalendarDays} />,
          },
          {
            label: "Risk Assessment",
            url: "/?path=/docs/programcard-programcard--docs",
            icon: <FontAwesomeIcon icon={faTriangleExclamation} />,
          },
          {
            label: "Program Performance",
            url: "/?path=/docs/programcard-programcard--docs",
            icon: <FontAwesomeIcon icon={faChartSimple} />,
          },
        ],
      },
      {
        label: "Program Links That Are Super Useful And Fun",
        items: [
          {
            label: "Management",
            url: "/?path=/docs/programcard-programcard--docs",
            icon: <FontAwesomeIcon icon={faDashboard} />,
          },
          {
            label: "Database This Is Also A Super Long Link Name",
            url: "/?path=/docs/programcard-programcard--docs",
            icon: <FontAwesomeIcon icon={faDatabase} />,
          },
        ],
      },
    ],
  },
  {
    label: "My Super Amazing Low Latency Database",
    icon: <FontAwesomeIcon icon={faDatabase} />,
    items: [],
  },
];

const meta: Meta<typeof SideBar> = {
  title: "SideBar",
  component: SideBar,
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
    header: "Storybook Side Bar Expandable Menu",
    menuLinks: MENU_LINKS,
  },
  render: (args) => {
    return (
      <>
        <style>
          {`
            [class*="side-bar_"] {
              margin-top: 0;
              height: 100%;
            }
            .sb-show-main {
              padding: 0 !important;
            }
          `}
        </style>
        <SideBar {...args} />
      </>
    );
  },
};
