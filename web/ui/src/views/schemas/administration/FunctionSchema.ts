import { RJSFSchema, UiSchema } from "@rjsf/utils";

export interface FunctionFormData {
  name: string;
  description: string;
}

export const functionSchema: RJSFSchema = {
  title: "Add Function",
  type: "object",
  properties: {
    name: {
      type: "string",
      title: "Name",
    },
    description: {
      type: "string",
      title: "Description",
    },
  },
  required: ["name", "description"],
};

export const functionUiSchema: UiSchema = {
  "ui:field": "LayoutGridField",
  "ui:layoutGrid": {
    "ui:row": {
      children: [
        {
          "ui:col": {
            sm: 6,
            children: ["name"],
          },
        },
        {
          "ui:col": {
            sm: 6,
            children: ["description"],
          },
        },
      ],
    },
  },
  name: {
    "ui:widget": "text",
    "ui:placeholder": "Enter Function Name",
    "ui:options": {
      label: true,
    },
  },
  description: {
    "ui:widget": "textarea",
    "ui:placeholder": "Enter description",
  },
};
