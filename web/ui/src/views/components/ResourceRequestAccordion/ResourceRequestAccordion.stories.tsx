import type { Meta, StoryObj } from "@storybook/react";
import React from "react";

import ResourceRequestAccordion from "views/components/ResourceRequestAccordion/ResourceRequestAccordion";

import { ITransitionGraph } from "definitions/portal/request/Transition.types.ts";

import {
  ActiveTransitions,
  ExampleRequest,
  ExampleTransitions,
} from "views/components/ResourceRequestAccordion/ResourceRequestAccordion.props";

interface ExampleChildProps {
  propMessage: string;
}

function ExampleChild({ propMessage }: ExampleChildProps) {
  return (
    <div
      style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}
      aria-description="My super fancy child"
    >
      <h1>Lorem Ipsum</h1>
      <button
        onClick={() => {
          alert(propMessage);
        }}
      >
        Click Me
      </button>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in
        venenatis enim. Proin bibendum nulla ac augue facilisis, at gravida eros
        dignissim. Sed a urna a nunc blandit bibendum. Vestibulum ante ipsum
        primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed in
        felis id sapien dictum viverra. Nulla facilisi. Integer posuere ligula
        nec nisi volutpat, nec vehicula libero efficitur. Vivamus et eros nec
        libero gravida ultricies.
      </p>
      <h2>Subheading</h2>
      <p>
        Donec sollicitudin nulla at erat dictum, ac pharetra nulla gravida.
        Maecenas fringilla turpis nec metus facilisis, at feugiat turpis
        gravida. Curabitur ut eros a felis fermentum cursus. Sed sit amet orci a
        lorem efficitur tincidunt. Fusce et orci nec turpis pharetra varius.
        Nulla facilisi. Aenean bibendum, ligula vel fermentum ultricies, velit
        justo fermentum velit, a tempor risus magna a metus.
      </p>
      <h3>Another Subheading</h3>
      <p>
        Praesent ac felis nec risus varius interdum. Phasellus et erat in turpis
        gravida aliquam. Vivamus euismod nisi non augue dapibus, vel fermentum
        eros varius. Nulla facilisi. Nam vel neque eu risus aliquet vehicula.
        Integer non orci quis ligula cursus pharetra. Integer ut magna sed metus
        feugiat fermentum.
      </p>
      <h4>Small Heading</h4>
      <p>
        Sed non urna nec nisi aliquet dapibus. In hac habitasse platea dictumst.
        Donec ac purus a felis interdum bibendum. Ut sit amet ligula vel orci
        fermentum gravida. Curabitur at erat nec libero ullamcorper venenatis.
        Aenean nec tortor sed libero efficitur varius. Aliquam erat volutpat.
        Donec convallis, risus a fringilla facilisis, metus est malesuada erat,
        nec tincidunt orci nisi non nulla.
      </p>
    </div>
  );
}

const meta: Meta<typeof ResourceRequestAccordion> = {
  title: "Accordions/ResourceRequestAccordion",
  component: ResourceRequestAccordion,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    thumbnailPath: "/thumbnail/default/l3harris_red_thumbnail.png",
    tooltipContent: null,
    locked: false,
    className: "",
  },
  render: (args) => (
    <ResourceRequestAccordion
      key={1}
      {...args}
      request={{
        ...ExampleRequest,
        transitions: ExampleTransitions["Default"],
      }}
    >
      {() => <ExampleChild propMessage="Clicked!" />}
    </ResourceRequestAccordion>
  ),
};

export const Revise: Story = {
  args: {
    thumbnailPath: "/thumbnail/default/l3harris_red_thumbnail.png",
    tooltipContent: (
      <>
        <h3>Tooltip Content</h3>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lectus
        felis, pharetra non nunc eget, semper iaculis purus. Proin rutrum est
        augue, id faucibus est ullamcorper vitae. Vestibulum sollicitudin nibh
        eget quam mattis elementum. Nulla facilisi. Curabitur ac magna
        efficitur, ornare nisl ac, faucibus purus. In eget erat mauris. Proin
        lacus elit, egestas sit amet aliquam ut, laoreet ut purus.
      </>
    ),
    locked: false,
    className: "",
  },
  render: (args) => (
    <ResourceRequestAccordion
      key={2}
      {...args}
      request={{
        ...ExampleRequest,
        transitions: ExampleTransitions["Revise"],
      }}
    >
      {() => <ExampleChild propMessage="Clicked!" />}
    </ResourceRequestAccordion>
  ),
};

export const BusinessProcessExpertApproved: Story = {
  args: {
    thumbnailPath: "/thumbnail/default/l3harris_red_thumbnail.png",
    tooltipContent: (
      <>
        <h3>Tooltip Content</h3>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lectus
        felis, pharetra non nunc eget, semper iaculis purus. Proin rutrum est
        augue, id faucibus est ullamcorper vitae. Vestibulum sollicitudin nibh
        eget quam mattis elementum. Nulla facilisi. Curabitur ac magna
        efficitur, ornare nisl ac, faucibus purus. In eget erat mauris. Proin
        lacus elit, egestas sit amet aliquam ut, laoreet ut purus.
      </>
    ),
    locked: true,
    className: "",
  },
  render: (args) => (
    <ResourceRequestAccordion
      key={3}
      {...args}
      request={{
        ...ExampleRequest,
        transitions: ExampleTransitions["BusinessProcessExpertApproved"],
      }}
    >
      {() => <ExampleChild propMessage="Clicked!" />}
    </ResourceRequestAccordion>
  ),
};

export const BusinessProcessExpertRejected: Story = {
  args: {
    thumbnailPath: "/thumbnail/default/l3harris_red_thumbnail.png",
    tooltipContent: (
      <>
        <h3>Tooltip Content</h3>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lectus
        felis, pharetra non nunc eget, semper iaculis purus. Proin rutrum est
        augue, id faucibus est ullamcorper vitae. Vestibulum sollicitudin nibh
        eget quam mattis elementum. Nulla facilisi. Curabitur ac magna
        efficitur, ornare nisl ac, faucibus purus. In eget erat mauris. Proin
        lacus elit, egestas sit amet aliquam ut, laoreet ut purus.
      </>
    ),
    locked: true,
    className: "",
  },
  render: (args) => (
    <ResourceRequestAccordion
      key={4}
      {...args}
      request={{
        ...ExampleRequest,
        transitions: ExampleTransitions["BusinessProcessExpertRejected"],
      }}
    >
      {() => <ExampleChild propMessage="Clicked!" />}
    </ResourceRequestAccordion>
  ),
};

export const SuperUserApproved: Story = {
  args: {
    thumbnailPath: "/thumbnail/default/l3harris_red_thumbnail.png",
    tooltipContent: (
      <>
        <h3>Tooltip Content</h3>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lectus
        felis, pharetra non nunc eget, semper iaculis purus. Proin rutrum est
        augue, id faucibus est ullamcorper vitae. Vestibulum sollicitudin nibh
        eget quam mattis elementum. Nulla facilisi. Curabitur ac magna
        efficitur, ornare nisl ac, faucibus purus. In eget erat mauris. Proin
        lacus elit, egestas sit amet aliquam ut, laoreet ut purus.
      </>
    ),
    locked: true,
    className: "",
  },
  render: (args) => (
    <>
      <ResourceRequestAccordion
        key={5}
        {...args}
        request={{
          ...ExampleRequest,
          transitions: ExampleTransitions["SuperUserApproved"],
        }}
      >
        {() => <ExampleChild propMessage="Clicked!" />}
      </ResourceRequestAccordion>
    </>
  ),
};

export const ActiveExample: Story = {
  args: {
    thumbnailPath: "/thumbnail/default/l3harris_red_thumbnail.png",
    tooltipContent: (
      <>
        <h3>Tooltip Content</h3>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lectus
        felis, pharetra non nunc eget, semper iaculis purus. Proin rutrum est
        augue, id faucibus est ullamcorper vitae. Vestibulum sollicitudin nibh
        eget quam mattis elementum. Nulla facilisi. Curabitur ac magna
        efficitur, ornare nisl ac, faucibus purus. In eget erat mauris. Proin
        lacus elit, egestas sit amet aliquam ut, laoreet ut purus.
      </>
    ),
    className: "",
  },

  render: (args) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [_, setCount] = React.useState(1);
    const [transitionGraph, setTransitionGraph] =
      React.useState<ITransitionGraph>({
        latest: 1,
        nodes: { 1: ActiveTransitions[0] },
      } as ITransitionGraph);

    // Add transitions to the component on an interval.
    React.useEffect(() => {
      const interval = setInterval(() => {
        setCount((prevCount) => {
          if (prevCount < ActiveTransitions.length) {
            const newCount = prevCount + 1;
            setTransitionGraph((prevTransitions) => ({
              latest: newCount,
              nodes: {
                ...prevTransitions.nodes,
                [newCount]: ActiveTransitions[newCount - 1],
              },
            }));
            return newCount;
          } else {
            setTransitionGraph({
              latest: 1,
              nodes: { 1: ActiveTransitions[0] },
            });
            return 1;
          }
        });
      }, 2000);

      return () => clearInterval(interval);
    }, []);

    return (
      <>
        <ResourceRequestAccordion
          key={6}
          {...args}
          request={{
            ...ExampleRequest,
            transitions: transitionGraph,
          }}
        >
          {() => <ExampleChild propMessage="Clicked!" />}
        </ResourceRequestAccordion>
      </>
    );
  },
};
