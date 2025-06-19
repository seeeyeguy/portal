import { RJSFSchema, UiSchema } from "@rjsf/utils";

export interface NewTagFormData {
  name: string;
  category?: string;
  subCategory?: string;
}

export const newTagSchema: RJSFSchema = {
  title: "Add Tag",
  type: "object",
  properties: {
    category: {
      type: "string",
      title: "Category",
      examples: [],
    },
    subCategory: {
      type: "string",
      title: "Sub-Category",
      examples: [],
    },
    name: {
      type: "string",
      title: "Name",
    },
  },
  required: ["name"],
};

export const newTagUiSchema: UiSchema = {
  "ui:field": "LayoutGridField",
  "ui:layoutGrid": {
    "ui:row": {
      children: [
        {
          "ui:columns": {
            xs: 6,
            children: ["category", "subCategory"],
          },
        },
        {
          "ui:col": {
            sm: 12,
            children: ["name"],
          },
        },
      ],
    },
  },
  category: {
    "ui:widget": "text",
    "ui:placeholder": "Select Category",
  },
  subCategory: {
    "ui:widget": "text",
    "ui:placeholder": "Select Sub-Category",
  },
  name: {
    "ui:widget": "text",
    "ui:placeholder": "Enter Tag Name",
  },
};
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function newTagCustomValidate(formData: NewTagFormData, errors: any) {
  if (formData.category && !formData.subCategory) {
    errors.subCategory.addError(
      "Sub-Category is required if a Category is used"
    );
  }
  if (!formData.category && formData.subCategory) {
    errors.category.addError("Category is required if a Sub-Category is used");
  }
  return errors;
}
