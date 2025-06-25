import { RJSFSchema, UiSchema } from "@rjsf/utils";

export interface TagFormData {
  name: string;
  category?: string;
  subCategory?: string;
}

export const tagSchema: RJSFSchema = {
  title: "Add Tag",
  type: "object",
  properties: {
    name: {
      type: "string",
      title: "Name",
    },
    category: {
      type: "string",
      title: "Category",
      examples: [], // Overwrite with Categories at render time.
    },
    subCategory: {
      type: "string",
      title: "Sub-Category",
      examples: [], // Overwrite with Sub-Categories at render time.
    },
  },
  required: ["name"],
};

export const tagUiSchema: UiSchema = {
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
            children: [],
          },
        },
        {
          "ui:columns": {
            sm: 6,
            children: ["category", "subCategory"],
          },
        },
      ],
    },
  },
  name: {
    "ui:widget": "text",
    "ui:placeholder": "Enter Tag Name",
  },
  category: {
    "ui:widget": "text",
    "ui:placeholder": "Select Category",
  },
  subCategory: {
    "ui:widget": "text",
    "ui:placeholder": "Select Sub-Category",
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function tagCustomValidate(formData: TagFormData, errors: any) {
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
