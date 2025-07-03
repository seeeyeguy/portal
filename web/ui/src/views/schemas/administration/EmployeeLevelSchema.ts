import { RJSFSchema, UiSchema } from "@rjsf/utils";
import UpDownWidget from "views/components/UpDownWidget/UpDownWidget";

export interface EmployeeLevelFormData {
  name: string;
  level: number;
  description: string;
}

export const employeeLevelSchema: RJSFSchema = {
  title: "Add Employee Level",
  type: "object",
  properties: {
    name: {
      type: "string",
      title: "Name",
    },
    level: {
      type: "number",
      title: "Employee Level",
    },
    description: {
      type: "string",
      title: "Description",
    },
  },
  required: ["name", "level", "description"],
};

export const employeeLevelUiSchema: UiSchema = {
  "ui:field": "LayoutGridField",
  "ui:layoutGrid": {
    "ui:row": {
      children: [
        {
          "ui:col": {
            sm: 6,
            children: ["name", "level"],
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
    "ui:placeholder": "Enter Employee Level Name",
  },
  level: {
    "ui:widget": "UpDownWidget",
    "ui:disabled": true,
    "ui:options": {
      min: 1,
      skipNumbers: [], // Numbers to skip
    },
  },
  description: {
    "ui:widget": "textarea",
  },
};

export const employeeLevelWidgets = {
  UpDownWidget,
};
