import Form from "@rjsf/primereact";
import { RJSFSchema, UiSchema } from "@rjsf/utils";
import validator from "@rjsf/validator-ajv8";
import type { Meta, StoryObj } from "@storybook/react";

const meta: Meta<typeof Form> = {
  title: "React JSON Schema Form/Example",
  component: Form,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const holidays = [
  "New Year's Day",
  "Valentine's Day",
  "Easter",
  "Independence Day",
  "Halloween",
  "Thanksgiving",
  "Christmas",
  "Labor Day",
  "Memorial Day",
  "Veterans Day",
];

const exampleSchema: RJSFSchema = {
  title: "Personal Info Form",
  type: "object",
  properties: {
    name: {
      type: "string",
      title: "Name",
    },
    email: {
      type: "string",
      format: "email",
      title: "Email",
    },
    birthDate: {
      type: "string",
      format: "date",
      title: "Birth Date",
    },
    password: {
      type: "string",
      title: "Password",
    },
    contactMethod: {
      type: "string",
      title: "Preferred Contact Method",
      enum: ["Email", "Phone", "Mail"],
    },
    favoriteColor: {
      type: "string",
      title: "Favorite Color",
      enum: ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"],
    },
    favoriteHoliday: {
      type: "string",
      title: "Favorite Holiday",
      examples: holidays,
      enum: holidays,
    },
    skills: {
      type: "array",
      title: "Skills",
      items: {
        type: "string",
        enum: ["JavaScript", "React", "Node.js", "CSS", "HTML"],
      },
      uniqueItems: true,
    },
    shoes: {
      type: "array",
      title: "Shoes",
      items: {
        type: "string",
        enum: ["Sandals", "Sneakers", "Boots", "Running", "Heels"],
      },
      uniqueItems: true,
    },
    bio: {
      type: "string",
      title: "Bio",
    },
    agreeToTerms: {
      type: "boolean",
      title: "Agree to Terms",
    },
  },
  required: ["name", "password", "agreeToTerms"],
};

const exampleUiSchema: UiSchema = {
  name: {
    "ui:widget": "text", // InputText as the default widget
    "ui:placeholder": "Enter your name",
  },
  email: {
    "ui:widget": "text", // InputText as the default widget
    "ui:placeholder": "Enter your email",
  },
  birthDate: {
    "ui:widget": "date",
    "ui:options": {
      yearsRange: [1900, 2020],
    },
  },
  password: {
    "ui:widget": "password", // Password as password widget
    "ui:placeholder": "Enter your password",
  },
  contactMethod: {
    "ui:widget": "radio", // RadioButton as radio widget
  },
  favoriteColor: {
    "ui:widget": "select", // Select as select widget
    "ui:placeholder": "Select your favorite color",
  },
  favoriteHoliday: {
    "ui:widget": "text", // Select as select widget
    "ui:placeholder": "Select your favorite holiday",
  },
  skills: {
    "ui:widget": "select", // MultiSelect as select widget with multiple options
    "ui:options": "multiple",
  },
  shoes: {
    "ui:widget": "checkboxes", // MultiSelect as checkboxes with multiple options
  },
  bio: {
    "ui:widget": "textarea", // InputTextarea as textarea widget
    "ui:placeholder": "Enter your bio",
  },
  agreeToTerms: {
    "ui:widget": "checkbox", // Checkbox for boolean fields and checkboxes widget
  },
};

// More exmaples can be found here.
// https://rjsf-team.github.io/react-jsonschema-form/
export const Default: Story = {
  args: {
    schema: exampleSchema,
    uiSchema: exampleUiSchema,
  },
  render: (args) => (
    <Form
      {...args}
      validator={validator}
      onChange={(e) => console.log("Form data onChange:", e.formData)}
      onSubmit={(formResult) => {
        console.log("Form data onSubmit:", formResult.formData);
      }}
    />
  ),
};
