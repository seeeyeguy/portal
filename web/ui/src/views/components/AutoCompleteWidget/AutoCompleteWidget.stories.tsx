import type { Meta, StoryObj } from "@storybook/react";
import Form from "@rjsf/primereact";
import { RJSFSchema, UiSchema } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";

import AutoCompleteWidget from "views/components/AutoCompleteWidget/AutoCompleteWidget";

const meta: Meta<typeof Form> = {
  title: "AutoCompleteWidget",
  component: Form,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const defaultSchema: RJSFSchema = {
  title: "AutoCompleteWidget Form",
  type: "object",
  properties: {
    textInput: {
      type: "string",
      title: "AutoCompleteWidget",
      examples: [],
    },
  },
};

const defaultUiSchema: UiSchema = {
  textInput: {
    "ui:widget": "AutoCompleteWidget",
  },
};

const fruits = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew"];

const fetchFruits = (searchTerm: string) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const filteredFruits = fruits.filter(fruit =>
        fruit.toLowerCase().includes(searchTerm.toLowerCase())
      );
      resolve(filteredFruits);
    }, 1000); 
  });
};

// More examples can be found here.
// https://rjsf-team.github.io/react-jsonschema-form/
export const Default: Story = {
  args: {
    schema: defaultSchema,
    uiSchema: defaultUiSchema,
  },
  render: (args) => {
    const updatedUiSchema = {
      ...defaultUiSchema,
      textInput: {
        ...defaultUiSchema.textInput,
        "ui:options": {
          completeMethod: (searchTerm: string) => {
            console.log("test:", fetchFruits(searchTerm));
            return fetchFruits(searchTerm);
          },
        },
      }
    }

    return (
      <Form
        {...args}
        uiSchema={updatedUiSchema}
        widgets={{ AutoCompleteWidget }}
        validator={validator}
        onChange={(e) => console.log("Form data onChange:", e.formData)}
        onSubmit={(formResult) => {
          console.log("Form data onSubmit:", formResult.formData);
        }}
      />
    );
  },
};