import Form from "@rjsf/primereact";
import { RJSFSchema, UiSchema } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";
import type { Meta, StoryObj } from "@storybook/react";

import TagSelectionWidget from "views/components/TagSelectionWidget/TagSelectionWidget";

const meta: Meta<typeof Form> = {
  title: "TagSelectionWidget",
  component: Form,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const tags = [
  {
    id: 1,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "filter::site:Location_1",
  },
  {
    id: 2,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "filter::site:Location_2",
  },
  {
    id: 3,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "filter::color:red",
  },
  {
    id: 4,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "filter::color:blue",
  },
  {
    id: 5,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "status::pending:true",
  },
  {
    id: 6,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "status::pending:false",
  },
  {
    id: 7,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "status::approved:false",
  },
  {
    id: 8,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "status::approved:true",
  },
  {
    id: 9,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "Cool",
  },
  {
    id: 10,
    created: "1970-01-01T12:00:00-04:00",
    modified: "1970-01-01T12:00:00-04:00",
    label: "Lame",
  },
];

const exampleSchema: RJSFSchema = {
  title: "TagSelectionWidget Form",
  type: "object",
  properties: {
    tagInput: {
      title: "TagSelectionWidget",
      type: "array",
      items: {
        type: "number",
      },
      uniqueItems: true,
    },
  },
};

const defaultUiSchema: UiSchema = {
  tagInput: {
    "ui:widget": "TagSelectionWidget",
    "ui:options": { tags },
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
      widgets={{ TagSelectionWidget }}
      validator={validator}
      onChange={(e) => console.log("Form data onChange:", e.formData)}
      onSubmit={(formResult) => {
        console.log("Form data onSubmit:", formResult.formData);
      }}
    />
  ),
};
