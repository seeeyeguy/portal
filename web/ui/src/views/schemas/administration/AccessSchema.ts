import { RJSFSchema, UiSchema } from "@rjsf/utils";

export interface AccessFormData {
  name: string;
  roleLevel?: number;
  subFunctions?: number[];
  stageLevels?: number[];
}

export const accessSchema: RJSFSchema = {
  title: "Add Access",
  type: "object",
  properties: {
    name: {
      type: "string",
      title: "Name",
      examples: [], // Overwrite with user emails at render time.
    },
    roleLevel: {
      type: "number",
      title: "Role",
      oneOf: [], // Overwrite with role levels at render time.
    },
    subFunctions: {
      type: "array",
      title: "Sub-Functions",
      items: {
        type: "number",
        anyOf: [], // Overwrite with Sub-Functions at render time.
      },
      uniqueItems: true,
    },
    stageLevels: {
      type: "array",
      title: "Stage Levels",
      items: {
        type: "number",
        anyOf: [], // Overwrite with Stage Levels at render time.
      },
      uniqueItems: true,
    },
  },
  required: ["name", "roleLevel"],
};

export const accessUiSchema: UiSchema = {
  "ui:field": "LayoutGridField",
  "ui:layoutGrid": {
    "ui:row": {
      children: [
        {
          "ui:columns": {
            sm: 6,
            children: ["name", "roleLevel"],
          },
        },
        {
          "ui:columns": {
            sm: 6,
            children: ["subFunctions", "stageLevels"],
          },
        },
      ],
    },
  },
  name: {
    "ui:widget": "text",
    "ui:placeholder": "Enter User Email",
  },
  roleLevel: {
    "ui:widget": "select",
    "ui:placeholder": "Select Role",
  },
  subFunctions: {
    "ui:widget": "select",
    "ui:placeholder": "Select Sub-Functions",
    "ui:options": "multiple",
  },
  stageLevels: {
    "ui:widget": "select",
    "ui:placeholder": "Select Stage Levels",
    "ui:options": "multiple",
  },
};
