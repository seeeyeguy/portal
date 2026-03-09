import { RJSFSchema, UiSchema } from "@rjsf/utils";

export interface MaintenanceBannerFormData {
  page: string;
  clone?: string;
  header: string;
  body: string;
  subtext: string;
  level: string;
  enabled: boolean;
  disableFunctionality: boolean;
  dismissable: boolean;
}

export const maintenanceBannerSchema: RJSFSchema = {
  title: "Add Maintenance Banner",
  type: "object",
  properties: {
    page: {
      type: "string",
      title: "Page",
      oneOf: [],
    },
    clone: {
      type: "string",
      title: "Clone From",
      oneOf: [],
    },
    header: {
      type: "string",
      title: "Header",
    },
    body: {
      type: "string",
      title: "Body",
    },
    subtext: {
      type: "string",
      title: "Subtext",
    },
    level: {
      type: "string",
      title: "Level",
      oneOf: [
        { const: "INFO", title: "Info" },
        { const: "SUCCESS", title: "Success" },
        { const: "WARNING", title: "Warning" },
        { const: "CRITICAL", title: "Critical" },
      ],
    },
    enabled: {
      type: "boolean",
      title: "Enabled",
      default: false,
    },
    disableFunctionality: {
      type: "boolean",
      title: "Disable Functionality",
      default: false,
    },
    dismissable: {
      type: "boolean",
      title: "Dismissable",
      default: false,
    },
  },
  required: ["page", "level", "enabled", "disableFunctionality", "dismissable"],
};

export const maintenanceBannerUiSchema: UiSchema = {
  "ui:field": "LayoutGridField",
  "ui:layoutGrid": {
    "ui:row": {
      children: [
        {
          "ui:col": {
            sm: 6,
            children: ["page", "clone", "level"],
          },
        },
        {
          "ui:col": {
            sm: 6,
            children: [
              "header",
              "body",
              "subtext",
              {
                "ui:row": {
                  children: [
                    {
                      "ui:col": {
                        sm: 6,
                        children: ["enabled", "dismissable"],
                      },
                    },
                    {
                      "ui:col": {
                        sm: 6,
                        children: ["disableFunctionality"],
                      },
                    },
                  ],
                },
              },
            ],
          },
        },
      ],
    },
  },
  page: {
    "ui:widget": "select",
    "ui:placeholder": "Enter Page",
    "ui:disabled": false,
  },
  clone: {
    "ui:widget": "hidden",
    "ui:placeholder": "Clone From",
    "ui:disabled": false,
  },
  level: {
    "ui:widget": "select",
    "ui:placeholder": "Select Level",
    "ui:help":
      "Info: Blue banner, Success: Green banner, Warning: Yellow banner, Critical: Red banner",
    "ui:disabled": false,
  },
  header: {
    "ui:widget": "text",
    "ui:disabled": false,
  },
  body: {
    "ui:widget": "textarea",
    "ui:disabled": false,
  },
  subtext: {
    "ui:widget": "text",
    "ui:disabled": false,
  },
  enabled: {
    "ui:widget": "checkbox",
    "ui:options": {
      label: "Enabled",
    },
  },
  disableFunctionality: {
    "ui:widget": "checkbox",
    "ui:options": {
      label: "Disable Functionality",
    },
  },
  dismissable: {
    "ui:widget": "checkbox",
    "ui:options": {
      label: "Dismissable",
    },
  },
  "ui:submitButtonOptions": {
    norender: true,
  },
};
