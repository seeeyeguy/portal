import { RJSFSchema, UiSchema } from "@rjsf/utils";

export interface SubFunctionFormData {
  name: string;
  function: number;
  description?: string;
}

export const subFunctionSchema: RJSFSchema = {
  title: "Add Sub Function",
  type: "object",
  properties: {
    name: {
      type: "string",
      title: "Name",
    },
    function: {
      type: "number",
      title: "Function",
      oneOf: [], // Overwrite with role levels at render time.
    },
    description: {
      type: "string",
      title: "Description",
    },
  },
  required: ["name", "function"],
};

export const subFunctionUiSchema: UiSchema = {
  "ui:field": "LayoutGridField",
  "ui:layoutGrid": {
    "ui:row": {
      children: [
        {
          "ui:columns": {
            sm: 6,
            children: ["name", "function"],
          },
        },
        {
          "ui:col": {
            sm: 12,
            children: ["description"],
          },
        },
      ],
    },
  },
  name: {
    "ui:widget": "text",
    "ui:placeholder": "Enter Sub-Function Name",
  },
  function: {
    "ui:widget": "select",
    "ui:placeholder": "Select Parent Function",
  },
  description: {
    "ui:widget": "textarea",
  },
};
