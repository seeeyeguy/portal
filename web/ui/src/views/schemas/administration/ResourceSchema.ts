import { RJSFSchema, UiSchema } from "@rjsf/utils";

import AutoCompleteWidget from "views/components/AutoCompleteWidget/AutoCompleteWidget";
import FileUploadWidget from "views/components/FileUploadWidget/FileUploadWidget";
import TagSelectionWidget from "views/components/TagSelectionWidget/TagSelectionWidget";

import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";
import { IResource } from "definitions/portal/directory/Resource.types";
import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { ITag } from "definitions/portal/directory/Tag.types";

import { getThumbnailPath } from "views/utils/ResourceLinksUtility";

export interface ResourceFormData {
  name: string;
  description: string;
  url: string;
  thumbnail?: string | null;
  employeeLevels: number[];
  subfunctions: number[];
  tags: number[];
  primaryPoc: string;
  secondaryPoc?: string;
  type: string;
  download: boolean;
}

export function transformResourceToFormData(
  resource: IResource
): ResourceFormData {
  return {
    name: resource.name,
    description: resource.description,
    url: resource.url,
    thumbnail: resource.thumbnail ? getThumbnailPath(resource) : undefined,
    employeeLevels: resource.employeeLevels.map(
      (level: IEmployeeLevel) => level.id
    ),
    subfunctions: resource.subfunctions.map(
      (subfunction: ISubFunction) => subfunction.id
    ),
    tags: resource.tags.map((tag: ITag) => tag.id),
    primaryPoc: resource.primaryPointOfContact,
    type: resource.type,
    download: resource.download,
  };
}

export const resourceSchema: RJSFSchema = {
  title: "Add Resource",
  type: "object",
  properties: {
    name: {
      title: "Name",
      type: "string",
    },
    description: {
      title: "Description",
      type: "string",
      minLength: 30,
    },
    url: {
      title: "URL",
      type: "string",
      format: "uri",
    },
    thumbnail: {
      title: "Thumbnail",
      type: "string",
      format: "data-url",
    },
    employeeLevels: {
      title: "Employee Levels",
      type: "array",
      items: {
        type: "number",
        anyOf: [], // Overwrite with Employee Levels at render time.
      },
      uniqueItems: true,
    },
    subfunctions: {
      title: "Sub-Functions",
      type: "array",
      items: {
        type: "number",
        anyOf: [], // Overwrite with Sub-Functions at render time.
      },
      uniqueItems: true,
    },
    tags: {
      title: "Tags",
      type: "array",
      items: {
        type: "number",
      },
      uniqueItems: true,
    },
    primaryPoc: {
      title: "Primary Point of Contact",
      type: "string",
      examples: [], // Overwrite with user emails at render time.
      format: "email",
    },
    secondaryPoc: {
      title: "Secondary Point of Contact (Comma-delimited list)",
      type: "string",
      examples: [], // Overwrite with user emails at render time.
    },
    type: {
      title: "Type",
      type: "string",
      oneOf: [], // Overwrite with Types at render time.
    },
    download: {
      title: "Download",
      type: "boolean",
      default: false,
    },
  },
  required: [
    "name",
    "url",
    "description",
    "primaryPoc",
    "employeeLevels",
    "subfunctions",
    "type",
  ],
};

export const resourceUiSchema: UiSchema = {
  "ui:field": "LayoutGridField",
  "ui:layoutGrid": {
    "ui:row": {
      size: {
        sm: 12,
      },
      children: [
        {
          "ui:col": {
            sm: 5,
            children: [
              "name",
              "url",
              "description",
              {
                "ui:row": {
                  children: [
                    {
                      "ui:col": {
                        sm: 6,
                        children: ["employeeLevels"],
                      },
                    },
                    {
                      "ui:col": {
                        sm: 6,
                        children: ["subfunctions"],
                      },
                    },
                  ],
                },
              },
              {
                "ui:row": {
                  children: [
                    {
                      "ui:col": {
                        sm: 6,
                        children: ["type"],
                      },
                    },
                    {
                      "ui:col": {
                        sm: 1,
                        children: [],
                      },
                    },
                    {
                      "ui:col": {
                        sm: 2,
                        children: ["download"],
                      },
                    },
                  ],
                },
              },
              "primaryPoc",
              "secondaryPoc",
            ],
          },
        },
        {
          "ui:col": {
            sm: 1,
            children: [],
          },
        },
        {
          "ui:col": {
            sm: 5,
            children: [
              {
                "ui:row": {
                  children: [
                    {
                      "ui:col": {
                        sm: 3,
                        children: [],
                      },
                    },
                    {
                      "ui:col": {
                        sm: 6,
                        children: ["thumbnail"],
                      },
                    },
                  ],
                },
              },
              {
                "ui:col": {
                  sm: 4,
                  children: ["tags"],
                },
              },
            ],
          },
        },
      ],
    },
  },
  name: {
    "ui:widget": "text",
    "ui:placeholder": "Enter Resource Name",
  },
  description: {
    "ui:widget": "textarea",
    "ui:placeholder": "Enter Description",
  },
  url: {
    "ui:widget": "text",
    "ui:placeholder": "Enter Resource URL",
  },
  thumbnail: {
    "ui:widget": "FileUploadWidget",
  },
  employeeLevels: {
    "ui:widget": "select",
    "ui:placeholder": "Select Employee Levels",
    "ui:options": "multiple",
  },
  tags: {
    "ui:widget": "TagSelectionWidget",
  },
  primaryPoc: {
    "ui:widget": "AutoCompleteWidget",
    "ui:placeholder": "Enter Primary POC",
  },
  secondaryPoc: {
    "ui:widget": "AutoCompleteWidget",
    "ui:placeholder": "Select Secondary POC",
  },
  type: {
    "ui:widget": "select",
    "ui:placeholder": "Select Resource Type",
  },
  download: {
    "ui:widget": "checkbox",
  },
};

export const resourceCustomValidate = (
  formData: ResourceFormData,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  errors: any
) => {
  if (formData.secondaryPoc && !validateEmailList(formData.secondaryPoc)) {
    errors.secondaryPoc.addError("One or more emails is invalid.");
  }

  if (formData.employeeLevels.length === 0) {
    errors.employeeLevels.addError(
      "must have at least one Employee Level selected"
    );
  }

  if (formData.subfunctions.length === 0) {
    errors.subfunctions.addError(
      "must have at least one Sub-Function selected"
    );
  }
  return errors;
};

const validateEmailList = (emailList: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const emails = emailList.split(",").map((email) => email.trim());
  const allValid = emails.every((email) => emailRegex.test(email));
  return allValid;
};

export const resourceWidgets = {
  AutoCompleteWidget,
  FileUploadWidget,
  TagSelectionWidget,
};
