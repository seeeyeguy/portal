import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";
import type { Meta, StoryObj } from "@storybook/react";

import {
  accessSchema,
  accessUiSchema,
} from "views/schemas/administration/AccessSchema";
import {
  employeeLevelSchema,
  employeeLevelUiSchema,
  employeeLevelWidgets,
} from "views/schemas/administration/EmployeeLevelSchema";
import {
  functionSchema,
  functionUiSchema,
} from "views/schemas/administration/FunctionSchema";
import {
  subFunctionSchema,
  subFunctionUiSchema,
} from "views/schemas/administration/SubFunctionSchema";
/*
import {
  resourceCustomValidate,
  resourceSchema,
  resourceUiSchema,
  resourceWidgets,
} from "views/schemas/administration/ResourceSchema";
*/
import {
  tagCustomValidate,
  tagSchema,
  tagUiSchema,
} from "views/schemas/administration/TagSchema";

const meta: Meta<typeof Form> = {
  title: "React JSON Schema Form / Administration",
  component: Form,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const TagFormSchema: Story = {
  args: {
    formData: {
      name: "Obi Wan",
      category: "Jedi",
      subCategory: "Master",
    },
    schema: tagSchema,
    uiSchema: tagUiSchema,
    customValidate: tagCustomValidate,
    showErrorList: false,
    noHtml5Validate: true,
  },
  render: (args) => {
    if (args.schema.properties) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.category as any).examples = ["Sith", "Jedi"];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.subCategory as any).examples = [
        "Master",
        "Apprentice",
        "Padawan",
      ];
    }

    return (
      <Form
        {...args}
        validator={validator}
        onChange={(e) => console.log("Form data onChange:", e.formData)}
        onSubmit={(formResult) => {
          console.log("Form data onSubmit:", formResult.formData);
          alert("Successfully Submitted Tag.");
        }}
      />
    );
  },
};

export const FunctionFormSchema: Story = {
  args: {
    formData: {
      name: "Sith Stories 2",
      function: 2,
      description:
        "Did you ever hear the Tragedy of Darth Plagueis the Wise? I thought not. It's not a story the Jedi would tell you. It's a Sith legend.",
    },
    schema: functionSchema,
    uiSchema: functionUiSchema,
    showErrorList: false,
    noHtml5Validate: true,
  },
  render: (args) => (
    <Form
      {...args}
      validator={validator}
      onChange={(e) => console.log("Form data onChange:", e.formData)}
      onSubmit={(formResult) => {
        console.log("Form data onSubmit:", formResult.formData);
        alert("Successfully Submitted Function.");
      }}
    />
  ),
};

export const SubFunctionFormSchema: Story = {
  args: {
    formData: {
      name: "Darth Plagueis",
      function: 2,
      description:
        "Darth Plagueis... was a Dark Lord of the Sith so powerful and so wise, he could use the Force to influence the midi-chlorians... to create... life. He had such a knowledge of the dark side, he could even keep the ones he cared about... from dying.",
    },
    schema: subFunctionSchema,
    uiSchema: subFunctionUiSchema,
    showErrorList: false,
    noHtml5Validate: true,
  },
  render: (args) => {
    if (args.schema.properties) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.function as any).oneOf = [
        { const: 1, title: "Jedi Stories 1" },
        { const: 2, title: "Sith Stories 2" },
      ];
    }

    return (
      <Form
        {...args}
        validator={validator}
        onChange={(e) => console.log("Form data onChange:", e.formData)}
        onSubmit={(formResult) => {
          console.log("Form data onSubmit:", formResult.formData);
          alert("Successfully Submitted SubFunction.");
        }}
      />
    );
  },
};

export const AccessFormSchema: Story = {
  args: {
    formData: {
      name: "Emperor.Palpatine@l3harris.com",
      roleLevel: 2,
      subFunctions: [1, 2],
      stageLevels: [1, 2, 3],
    },
    schema: accessSchema,
    uiSchema: accessUiSchema,
    showErrorList: false,
    noHtml5Validate: true,
  },
  render: (args) => {
    if (args.schema.properties) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.name as any).examples = [
        "Darth.Vader@l3harris.com",
        "Emperor.Palpatine@l3harris.com",
      ];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.roleLevel as any).oneOf = [
        { const: 1, title: "Emperor" },
        { const: 2, title: "Sith Apprentice" },
        { const: 3, title: "Stormtrooper" },
      ];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.subFunctions as any).items.anyOf = [
        { const: 1, title: "Sith Plans" },
        { const: 2, title: "Building Plans" },
        { const: 3, title: "Patrol Routes" },
      ];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.stageLevels as any).items.anyOf = [
        { const: 1, title: "Palaces" },
        { const: 2, title: "Secret Bases" },
        { const: 3, title: "Mega Constructions" },
      ];
    }

    return (
      <Form
        {...args}
        validator={validator}
        onChange={(e) => console.log("Form data onChange:", e.formData)}
        onSubmit={(formResult) => {
          console.log("Form data onSubmit:", formResult.formData);
          alert("Successfully Submitted Access.");
        }}
      />
    );
  },
};

export const EmployeeLevelFormSchema: Story = {
  args: {
    formData: {
      name: "Master Sith",
      description: "He has mastered all the power of the dark side.",
      level: [66],
    },
    schema: employeeLevelSchema,
    uiSchema: employeeLevelUiSchema,
    showErrorList: false,
    noHtml5Validate: true,
    widgets: employeeLevelWidgets,
  },
  render: (args) => {
    if (args.uiSchema) {
      args.uiSchema.level["ui:options"].skipNumbers = [2, 64, 65];
    }

    return (
      <Form
        {...args}
        validator={validator}
        onChange={(e) => console.log("Form data onChange:", e.formData)}
        onSubmit={(formResult) => {
          console.log("Form data onSubmit:", formResult.formData);
          alert("Successfully Submitted EmployeeLevel.");
        }}
      />
    );
  },
};

/*
export const ResourceFormSchema: Story = {
  args: {
    formData: {
      name: "My Galactic Resource",
      description: "Super Fancy Galactic Resource",
      previousRevision: 1,
      url: "http://example.com",
      thumbnail: null,
      employeeLevels: [1, 2],
      subFunctions: [2, 3],
      tags: [2, 5],
      primaryPoc: "Luke.Skywalker@l3harris.com",
      secondaryPoc: ["Leia.Organa@l3harris.com", "Han.Solo@l3harris.com"],
      type: "Kyber",
      download: true,
    },
    schema: resourceSchema,
    uiSchema: resourceUiSchema,
    customValidate: resourceCustomValidate,
    showErrorList: false,
    noHtml5Validate: true,
    widgets: resourceWidgets,
  },
  render: (args) => {
    if (args.schema.properties) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.primaryPoc as any).examples = [
        "Darth.Vader@l3harris.com",
        "Emperor.Palpatine@l3harris.com",
      ];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.secondaryPoc as any).examples = [
        "Darth.Vader@l3harris.com",
        "Emperor.Palpatine@l3harris.com",
      ];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.employeeLevels as any).items.anyOf = [
        { const: 1, title: "Emperor" },
        { const: 2, title: "Sith Apprentice" },
        { const: 3, title: "Stormtrooper" },
      ];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.subFunctions as any).items.anyOf = [
        { const: 1, title: "Sith Plans" },
        { const: 2, title: "Building Plans" },
        { const: 3, title: "Patrol Routes" },
      ];

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (args.schema.properties.type as any).oneOf = [
        { const: "Kyber", title: "Kyber" },
        { const: "Beskar", title: "Beskar" },
        { const: "Kalkite", title: "Kalkite" },
      ];
    }

    if (args.uiSchema) {
      args.uiSchema.tags["ui:options"] = {
        tags: [
          {
            id: 1,
            created: "1970-01-01T12:00:00-04:00",
            modified: "1970-01-01T12:00:00-04:00",
            label: "lightsaber::color:red",
          },
          {
            id: 2,
            created: "1970-01-01T12:00:00-04:00",
            modified: "1970-01-01T12:00:00-04:00",
            label: "lightsaber::color:blue",
          },
          {
            id: 3,
            created: "1970-01-01T12:00:00-04:00",
            modified: "1970-01-01T12:00:00-04:00",
            label: "lightsaber::color:green",
          },
          {
            id: 4,
            created: "1970-01-01T12:00:00-04:00",
            modified: "1970-01-01T12:00:00-04:00",
            label: "blaster::color:blue",
          },
          {
            id: 5,
            created: "1970-01-01T12:00:00-04:00",
            modified: "1970-01-01T12:00:00-04:00",
            label: "blaster::color:red",
          },
        ],
      };
    }

    return (
      <Form
        {...args}
        validator={validator}
        onChange={(e) => console.log("Form data onChange:", e.formData)}
        onSubmit={(formResult) => {
          console.log("Form data onSubmit:", formResult.formData);
          alert("Successfully Submitted Resource.");
        }}
      />
    );
  },
};
*/
