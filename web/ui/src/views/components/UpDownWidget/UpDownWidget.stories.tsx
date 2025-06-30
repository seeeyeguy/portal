import type { Meta, StoryObj } from "@storybook/react";
import Form from "@rjsf/primereact";
import { RJSFSchema, UiSchema } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";

import UpDownWidget from "views/components/UpDownWidget/UpDownWidget";

const meta: Meta<typeof Form> = {
  title: "UpDownWidget",
  component: Form,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const exampleSchema: RJSFSchema = {
  title: "UpDownWidget Form",
  type: "object",
  properties: {
    numberInput: {
      type: "number",
      title: "UpDownWidget",
    },
  },
};

const defaultUiSchema: UiSchema = {
  numberInput: {
    "ui:widget": "UpDownWidget",
    "ui:options": {},
  },
};

const SkipNumbersUiSchema: UiSchema = {
  numberInput: {
    "ui:widget": "UpDownWidget",
    "ui:options": {
      min: 0,
      skipNumbers: [1, 3, 5], // Numbers to skip.
    },
  },
};

// More exmaples can be found here.
// https://rjsf-team.github.io/react-jsonschema-form/
export const Default: Story = {
  args: {
    schema: exampleSchema,
    uiSchema: defaultUiSchema,
  },
  render: (args) => (
    <Form
      {...args}
      widgets={{ UpDownWidget }}
      validator={validator}
      onChange={(e) => console.log("Form data onChange:", e.formData)}
      onSubmit={(formResult) => {
        console.log("Form data onSubmit:", formResult.formData);
      }}
    />
  ),
};

// More exmaples can be found here.
// https://rjsf-team.github.io/react-jsonschema-form/
export const SkipNumbers: Story = {
  args: {
    schema: exampleSchema,
    uiSchema: SkipNumbersUiSchema,
  },
  render: (args) => (
    <Form
      {...args}
      widgets={{ UpDownWidget }}
      validator={validator}
      onChange={(e) => console.log("Form data onChange:", e.formData)}
      onSubmit={(formResult) => {
        console.log("Form data onSubmit:", formResult.formData);
      }}
    />
  ),
};
