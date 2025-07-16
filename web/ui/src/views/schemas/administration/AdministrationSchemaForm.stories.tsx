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
import {
  resourceCustomValidate,
  resourceSchema,
  resourceUiSchema,
  resourceWidgets,
} from "views/schemas/administration/ResourceSchema";
import {
  tagCustomValidate,
  tagSchema,
  tagUiSchema,
} from "views/schemas/administration/TagSchema";

import { base64ToFileUploadFile } from "views/utils/ImageUtility";

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
      subcategory: "Master",
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
      (args.schema.properties.subcategory as any).examples = [
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

export const ResourceFormSchema: Story = {
  args: {
    formData: {
      name: "My Galactic Resource",
      description: "Super Fancy Galactic Resource",
      previousRevision: 1,
      url: "http://example.com",
      thumbnail: base64ToFileUploadFile(
        "data:image/png;base64,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"
      ),
      employeeLevels: [1, 2],
      subfunctions: [2, 3],
      tags: [2, 5],
      primaryPoc: "Luke.Skywalker@l3harris.com",
      secondaryPoc: [
        "Leia.Organa@l3harris.com",
        "Han.Solo@l3harris.com",
      ].join(),
      type: "Kyber",
      download: true,
    },
    schema: resourceSchema,
    uiSchema: resourceUiSchema,
    showErrorList: false,
    noHtml5Validate: true,
    widgets: resourceWidgets,
    customValidate: resourceCustomValidate,
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
      (args.schema.properties.subfunctions as any).items.anyOf = [
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
