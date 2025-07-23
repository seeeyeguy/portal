import { BrowserRouter as Router } from "react-router-dom";
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

const DEFAULT_MENU_LINKS: IMenuLink[] = [
  {
    label: "Administration",
    icon: <FontAwesomeIcon icon={faListCheck} />,
    items: [
      {
        label: "Add Resource",
        command: () => console.log("TEST"),
      },
      {
        label: "Approve Request",
        command: () => console.log("TEST"),
        icon: <FontAwesomeIcon icon={faSquareCheck} />,
      },
    ],
    path: null,
    customContent: (
      <div
        aria-description="test links"
        style={{ display: "flex", flexDirection: "column", flex: 1 }}
      >
        <a href="#">How to approve a resource?</a>
        <a href="#">Where to get permissions?</a>
        <a href="#">Who is my admin?</a>
        <hr></hr>
        <a href="#">My Links</a>
        <a href="#">My Tools</a>
        <a href="#">My Favorites</a>
        <hr></hr>
        <a href="#">My Links</a>
        <a href="#">My Tools</a>
        <a href="#">My Favorites</a>
      </div>
    ),
  },
  {
    label: "Program",
    icon: <FontAwesomeIcon icon={faChartLine} />,
    path: null,
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
    path: null,
  },
];

const TOP_LEVEL_MENU_LINKS: IMenuLink[] = [
  {
    label: "Administration",
    icon: <FontAwesomeIcon icon={faListCheck} />,
    path: null,
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
        <a href="#">How to approve a resource?</a>
        <a href="#">Where to get permissions?</a>
        <a href="#">Who is my admin?</a>
        <hr></hr>
        <a href="#">My Links</a>
        <a href="#">My Tools</a>
        <a href="#">My Favorites</a>
        <hr></hr>
        <a href="#">My Links</a>
        <a href="#">My Tools</a>
        <a href="#">My Favorites</a>
      </div>
    ),
  },
  {
    label: "PRT",
    url: "/?path=/docs/programcard-programcard",
    icon: <FontAwesomeIcon icon={faCalendarDays} />,
    path: null,
  },
  {
    label: "Risk Assessment",
    url: "/?path=/docs/programcard-programcard",
    icon: <FontAwesomeIcon icon={faTriangleExclamation} />,
    path: null,
  },
  {
    label: "Program Performance",
    url: "/?path=/docs/programcard-programcard",
    icon: <FontAwesomeIcon icon={faChartSimple} />,
    path: null,
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
    menuLinks: DEFAULT_MENU_LINKS,
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
        <Router>
          <SideBar {...args} />
        </Router>
      </>
    );
  },
};

export const TopLevelLinks: Story = {
  args: {
    menuLinks: TOP_LEVEL_MENU_LINKS,
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
        <Router>
          <SideBar {...args} />
        </Router>
      </>
    );
  },
};
