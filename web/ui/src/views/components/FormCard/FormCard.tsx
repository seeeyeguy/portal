import React from "react";

import Form, { FormProps } from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";

import styles from "views/components/FormCard/FormCard.module.css";

export interface IFormCardProps {
  /** Optional props for the `Form` component. */
  formProps?: FormProps;

  /** Optional callback to invoke when the `Delete`/`Revoke` button is clicked. */
  onDelete?: () => void;

  /** Optional callback to invoke when the `Update` button is clicked. */
  onSubmit?: () => Promise<void> | void;

  /** Optional label for the `Delete`/`Revoke` button. */
  updateButtonLabel?: string;

  /** Optional label for the `Update` button. */
  deleteButtonLabel?: string;
}

const DEFAULT_FORM_PROPS: FormProps = {
  schema: {},
  uiSchema: {
    "ui:submitButtonOptions": {
      norender: true,
    },
  },
  validator: validator,
  showErrorList: false,
  noHtml5Validate: true,
};

export default function FormCard({
  formProps = DEFAULT_FORM_PROPS,
  onDelete,
  onSubmit,
  updateButtonLabel = "Update",
  deleteButtonLabel = "Delete",
}: IFormCardProps) {
  const formRef = React.useRef<Form | null>(null);

  const handleUpdate = React.useCallback(() => {
    if (formRef?.current) {
      formRef?.current?.submit();
    }
  }, [formRef]);

  return (
    <section
      className={`${styles["form-card"]}`}
      aria-description="container for form information"
    >
      <div
        className={`${styles["form-container"]}`}
        aria-description="container for form component"
      >
        <Form
          onSubmit={onSubmit}
          ref={formRef}
          {...{ ...DEFAULT_FORM_PROPS, ...formProps }}
        />
      </div>
      <div
        className={`${styles["button-container"]}`}
        aria-description="container for button components"
      >
        {onDelete && (
          <button
            className={styles["delete-form-card-button"]}
            onClick={() => onDelete()}
            aria-label="delete form card button"
          >
            {deleteButtonLabel}
          </button>
        )}
        {onSubmit && (
          <button
            className={styles["update-form-card-button"]}
            onClick={() => handleUpdate()}
            aria-label="update form card button"
          >
            {updateButtonLabel}
          </button>
        )}
      </div>
    </section>
  );
}
