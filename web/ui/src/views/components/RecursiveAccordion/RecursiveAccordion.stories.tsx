import type { Meta, StoryObj } from "@storybook/react";

import RecursiveAccordion from "views/components/RecursiveAccordion/RecursiveAccordion";
import { PagedItemContainer } from "adas-react-components";

import { PagedItemContainerProps } from "adas-react-components/types";

import { FavoriteThumbnailLink } from "adas-react-components";

const bookmarks = [
  {
    name: "Google",
    href: "https://www.google.com/",
  },
  {
    name: "Stack Overflow",
    href: "https://stackoverflow.com/",
  },
  {
    name: "L3Harris",
    href: "https://mynexus.l3harris.com/",
  },
  {
    name: "Next.js",
    href: "https://nextjs.org/",
  },
  {
    name: "React",
    href: "https://react.dev/",
  },
  {
    name: "Laws of UX",
    href: "https://lawsofux.com/",
  },
  {
    name: "Python",
    href: "https://www.python.org/",
  },
  {
    name: "Tableau",
    href: "https://www.tableau.com/",
  },
  {
    name: "Ferrari",
    href: "https://www.ferrari.com/en-US",
  },
  {
    name: "L3Harris Code of Ethics",
    href: "https://mynexus.l3harris.com/Functions/Ethics/Pages/codeofethics",
  },
  {
    name: "L3Harris Community",
    href: "https://mynexus.l3harris.com/Functions/community",
  },
  {
    name: "L3Harris Ethics",
    href: "https://mynexus.l3harris.com/Functions/Ethics",
  },
  {
    name: "JavaScript",
    href: "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
  },
  {
    name: "GitHub",
    href: "https://github.com/",
  },
  {
    name: "W3Schools",
    href: "https://www.w3schools.com/",
  },
  {
    name: "Node.js",
    href: "https://nodejs.org/",
  },
  {
    name: "Docker",
    href: "https://www.docker.com/",
  },
  {
    name: "Visual Studio Code",
    href: "https://code.visualstudio.com/",
  },
  {
    name: "Tailwind CSS",
    href: "https://tailwindcss.com/",
  },
  {
    name: "Jest",
    href: "https://jestjs.io/",
  },
  {
    name: "Babel",
    href: "https://babeljs.io/",
  },
  {
    name: "Webpack",
    href: "https://webpack.js.org/",
  },
  {
    name: "NPM",
    href: "https://www.npmjs.com/",
  },
  {
    name: "ESLint",
    href: "https://eslint.org/",
  },
  {
    name: "Bitbucket",
    href: "https://lnsvr0329.gcsd.harris.com:8443/bitbucket/dashboard",
  },
  {
    name: "Confluence",
    href: "https://confluenceopen01.gs.myharris.net/login.action?os_destination=%2Findex.action&permissionViolation=true",
  },
  {
    name: "L3Harris Shop",
    href: "https://l3harris.geigershops.com/L3HC/homeprimary",
  },
  {
    name: "Bing",
    href: "https://www.bing.com/",
  },
  {
    name: "Firefox",
    href: "https://www.mozilla.org/en-US/firefox/new/",
  },
  {
    name: "Dot Net",
    href: "https://dotnet.microsoft.com/en-us/languages/csharp",
  },
  {
    name: "Express",
    href: "https://expressjs.com/",
  },
  {
    name: "Django",
    href: "https://www.djangoproject.com/",
  },
  {
    name: "Flask",
    href: "https://flask.palletsprojects.com/",
  },
  {
    name: "Ruby on Rails",
    href: "https://rubyonrails.org/",
  },
  {
    name: "Bootstrap",
    href: "https://getbootstrap.com/",
  },
  {
    name: "Foundation",
    href: "https://get.foundation/",
  },
  {
    name: "Angular",
    href: "https://angular.io/",
  },
  {
    name: "Vue.js",
    href: "https://vuejs.org/",
  },
  {
    name: "Electron",
    href: "https://www.electronjs.org/",
  },
  {
    name: "GraphQL",
    href: "https://graphql.org/",
  },
  {
    name: "MongoDB",
    href: "https://www.mongodb.com/",
  },
  {
    name: "MySQL",
    href: "https://www.mysql.com/",
  },
  {
    name: "PostgreSQL",
    href: "https://www.postgresql.org/",
  },
  {
    name: "SQLite",
    href: "https://www.sqlite.org/index.html",
  },
  {
    name: "Linux Foundation",
    href: "https://www.linuxfoundation.org/",
  },
  {
    name: "Kubernetes",
    href: "https://kubernetes.io/",
  },
  {
    name: "Terraform",
    href: "https://www.terraform.io/",
  },
  {
    name: "Jenkins",
    href: "https://www.jenkins.io/",
  },
  {
    name: "Ansible",
    href: "https://www.ansible.com/",
  },
  {
    name: "Firebase",
    href: "https://firebase.google.com/",
  },
  {
    name: "Heroku",
    href: "https://www.heroku.com/",
  },
  {
    name: "Netlify",
    href: "https://www.netlify.com/",
  },
  {
    name: "Vercel",
    href: "https://vercel.com/",
  },
  {
    name: "AWS (Amazon Web Services)",
    href: "https://aws.amazon.com/",
  },
  {
    name: "Google Cloud Platform",
    href: "https://cloud.google.com/",
  },
  {
    name: "Microsoft Azure",
    href: "https://azure.microsoft.com/",
  },
  {
    name: "DigitalOcean",
    href: "https://www.digitalocean.com/",
  },
  {
    name: "GitLab",
    href: "https://gitlab.com/",
  },
  {
    name: "Bitbucket",
    href: "https://bitbucket.org/",
  },
  {
    name: "Codecademy",
    href: "https://www.codecademy.com/",
  },
  {
    name: "freeCodeCamp",
    href: "https://www.freecodecamp.org/",
  },
  {
    name: "HackerRank",
    href: "https://www.hackerrank.com/",
  },
  {
    name: "LeetCode",
    href: "https://leetcode.com/",
  },
  {
    name: "Udemy",
    href: "https://www.udemy.com/",
  },
  {
    name: "Coursera",
    href: "https://www.coursera.org/",
  },
  {
    name: "Kaggle",
    href: "https://www.kaggle.com/",
  },
  {
    name: "Medium (Programming)",
    href: "https://medium.com/tag/programming",
  },
  {
    name: "Dev.to",
    href: "https://dev.to/",
  },
  {
    name: "Smashing Magazine",
    href: "https://www.smashingmagazine.com/",
  },
  {
    name: "CodePen",
    href: "https://codepen.io/",
  },
];

type Bookmark = (typeof bookmarks)[0];

const createDataSet = (
  bookmarks: Bookmark[],
  component: "link" | "thumbnail link",
  count: number
): React.ReactElement<unknown>[] => {
  const createLink = (bookmark: Bookmark): React.ReactElement<unknown> => (
    <a href={bookmark.href}>{bookmark.name}</a>
  );

  const createThumbnailLink = (
    bookmark: Bookmark
  ): React.ReactElement<unknown> => (
    <FavoriteThumbnailLink
      name={bookmark.name}
      description={bookmark.name}
      url={bookmark.href}
      thumbnail="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS31aMSQ0RDmKTdTF7-k6AH7WRwW4SHr9LemQ&s"
      imgWidth={95}
      imgHeight={95}
      target="_blank"
      isButtonActive={false}
      isButtonDisabled={false}
      buttonClassName=""
      buttonCallback={() => undefined}
      buttonErrorCallback={() => undefined}
    />
  );

  const componentFunction =
    component === "link" ? createLink : createThumbnailLink;

  return bookmarks.slice(0, count).map(componentFunction);
};

const meta = {
  title: "Accordions/RecursiveAccordion",
  component: RecursiveAccordion,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
    layout: "padded",
  },
} as Meta<typeof RecursiveAccordion>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: "Bookmarks",
    dataSet: {
      Websites: [],
      Links: [],
      Favorites: [],
    },
    recursionDepth: 0,
    isLoading: false,
    className: "",
    AccordionHeaderContent: [<></>],
  },
  render: (args) => (
    <RecursiveAccordion {...args}>
      {(props: unknown) => (
        <PagedItemContainer {...(props as PagedItemContainerProps)} />
      )}
    </RecursiveAccordion>
  ),
};

export const Bookmarks: Story = {
  args: {
    title: "Bookmarks",
    dataSet: {
      Websites: bookmarks,
      Links: bookmarks,
      Favorites: bookmarks,
    },
    recursionDepth: 0,
    isLoading: false,
    className: "",
    AccordionHeaderContent: [<></>],
  },
  render: (args) => (
    <>
      <style>
        {`.bookmarks-accordion section {
          border: 2px solid transparent;
      }`}
      </style>
      <RecursiveAccordion {...args} className="bookmarks-accordion">
        {(props: unknown) => (
          <PagedItemContainer
            dataSet={createDataSet(
              (props as { dataSet: (typeof bookmarks)[0][] }).dataSet,
              "thumbnail link",
              50
            )}
          />
        )}
      </RecursiveAccordion>
    </>
  ),
};

export const AccordionHeaderContent: Story = {
  args: {
    title: "Bookmarks",
    dataSet: {
      Websites: [],
      Links: [],
      Favorites: [],
    },
    recursionDepth: 0,
    isLoading: false,
    className: "",
    AccordionHeaderContent: [<></>],
  },
  render: (args) => (
    <RecursiveAccordion {...args}>
      {(props: unknown) => (
        <PagedItemContainer {...(props as PagedItemContainerProps)} />
      )}
    </RecursiveAccordion>
  ),
};

export const LoadingContent: Story = {
  args: {
    title: "Bookmarks",
    dataSet: {
      Websites: [],
      Links: [],
      Favorites: [],
    },
    recursionDepth: 0,
    isLoading: true,
    className: "",
    AccordionHeaderContent: [<></>],
  },
  render: (args) => (
    <RecursiveAccordion {...args}>
      {(props: unknown) => (
        <PagedItemContainer {...(props as PagedItemContainerProps)} />
      )}
    </RecursiveAccordion>
  ),
};
