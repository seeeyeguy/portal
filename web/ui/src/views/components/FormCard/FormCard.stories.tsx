import { FormProps } from "@rjsf/core";
import { RJSFSchema} from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";
import type { Meta, StoryObj } from "@storybook/react";

import FormCard from "views/components/FormCard/FormCard";

const meta: Meta<typeof FormCard> = {
  title: "FormCard/FormCard",
  component: FormCard,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

const exampleSchema: RJSFSchema = {
  title: "A text input field",
  type: "string",
};

const formProps:FormProps = {
  schema: exampleSchema,
  validator: validator,
  formData: "Test",
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {    
    onDelete: () => console.log("Test Delete."),
    onSubmit: () => console.log("Test Update."),    
  },
  render: (args) => {
    return <FormCard {...args} formProps={formProps}/>;
  },
};

export const HideUpdate: Story = {
  args: {
    onDelete: () => console.log("Test Delete."),
  },
  render: (args) => {
    return <FormCard {...args}  formProps={formProps} />;
  },
};
