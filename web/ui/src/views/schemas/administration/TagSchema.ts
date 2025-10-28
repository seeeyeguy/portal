import { RJSFSchema, UiSchema } from "@rjsf/utils";

export interface TagFormData {
  name: string;
  category?: string;
  subcategory?: string;
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
      title: "Category (optional)",
      examples: [], // Overwrite with Categories at render time.
    },
    subcategory: {
      type: "string",
      title: "Sub-Category (optional)",
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
            sm: 3,
            children: ["name"],
          },
        },
        {
          "ui:col": {
            sm: 4,
            children: ["category"],
          },
        },
        {
          "ui:col": {
            sm: 4,
            children: ["subcategory"],
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
  subcategory: {
    "ui:widget": "text",
    "ui:placeholder": "Select Sub-Category",
  },
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function tagCustomValidate(formData: TagFormData, errors: any) {
  if (formData.category && !formData.subcategory) {
    errors.subcategory.addError(
      "Sub-Category is required if a Category is used"
    );
  }
  if (!formData.category && formData.subcategory) {
    errors.category.addError("Category is required if a Sub-Category is used");
  }
  return errors;
}
