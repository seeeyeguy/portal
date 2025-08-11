import React from "react";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import FormType from "@rjsf/core";
import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import FormCard from "views/components/FormCard/FormCard";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";
import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";

import {
  EmployeeLevelFormData,
  employeeLevelSchema,
  employeeLevelUiSchema,
  employeeLevelWidgets,
} from "views/schemas/administration/EmployeeLevelSchema";

import {
  TApiPostEmployeeLevelRequest,
  TApiPutEmployeeLevelRequest,
  useAddEmployeeLevelMutation,
  useRemoveEmployeeLevelMutation,
  useGetEmployeeLevelsAdminQuery,
  useUpdateEmployeeLevelMutation,
} from "state/query/api/portal/directory/EmployeeLevelApi";

import { resolveApiErrorMessage } from "utils/PromiseUtility";

import styles from "views/containers/AdminControls/AdminControls.module.css";

export default function EmployeeLevelsControls() {
  const { data: employeeLevels, isLoading } =
    useGetEmployeeLevelsAdminQuery(null);

  const [addEmployeeLevel] = useAddEmployeeLevelMutation();
  const [updateEmployeeLevel] = useUpdateEmployeeLevelMutation();
  const [removeEmployeeLevel] = useRemoveEmployeeLevelMutation();

  const [showAddModal, setShowAddModal] = React.useState(false);
  const [showUpdateModal, setShowUpdateModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);

  const [tempFormData, setTempFormData] =
    React.useState<EmployeeLevelFormData | null>(null);
  const [tempFormId, setTempFormId] = React.useState<number | null>(null);

  const newFormRef = React.useRef<FormType>(null);
  const [newFormKey, setNewFormKey] = React.useState(Date.now());

  // Schema Options.
  const updatedUiSchema = React.useMemo(() => {
    if (employeeLevels?.data) {
      return {
        "ui:submitButtonOptions": {
          norender: true,
        },
        ...employeeLevelUiSchema,
        level: {
          ...employeeLevelUiSchema.level,
          "ui:disabled": false,
          "ui:options": {
            ...employeeLevelUiSchema.level["ui:options"],
            skipNumbers: (employeeLevels.data as IEmployeeLevel[]).map(
              (employeeLevel) => employeeLevel.level
            ),
          },
        },
      };
    }
    return employeeLevelUiSchema;
  }, [employeeLevels]);

  const handleCreate = React.useCallback(async () => {
    if (newFormRef.current && newFormRef.current.validateForm()) {
      const formSubmission: EmployeeLevelFormData = {
        ...newFormRef.current.state.formData,
      };

      // Create request body.
      const body: TApiPostEmployeeLevelRequest = {
        ...(formSubmission as TApiPostEmployeeLevelRequest),
      };

      const response = await addEmployeeLevel(body);

      // Handle the create API error.
      if (response.error) {
        const message =
          "data" in response.error
            ? resolveApiErrorMessage(response.error.data as string | object)
            : DEFAULT_API_ERROR_MESSAGE;

        toast.error(`Error creating employee level: ${message}`);
      } else {
        toast.success(`Employee Level Created`);
        // Reset form on success.
        setShowAddModal(false);
        setNewFormKey(Date.now());
      }
    }
  }, [addEmployeeLevel]);

  // Clear new employee level form to empty.
  const handleCancel = React.useCallback(() => {
    setShowAddModal(false);
    setNewFormKey(Date.now());
  }, []);

  const handleUpdate = React.useCallback(
    async (id: number | null, submittedData: EmployeeLevelFormData | null) => {
      if (id && submittedData) {
        const formSubmission: EmployeeLevelFormData = {
          ...submittedData,
        };

        // Create request body.
        const body: TApiPutEmployeeLevelRequest = {
          name: formSubmission.name,
          description: formSubmission.description,
        };

        const response = await updateEmployeeLevel({ body, id });

        // Handle the update API error.
        if (response.error) {
          const message =
            "data" in response.error
              ? resolveApiErrorMessage(response.error.data as string | object)
              : DEFAULT_API_ERROR_MESSAGE;

          toast.error(`Error updating employee level: ${message}`);
        } else {
          toast.success(`Employee Level Updated`);
          // Reset form on success.
          setShowUpdateModal(false);
          setTempFormData(null);
          setTempFormId(null);
        }
      }
    },
    [updateEmployeeLevel]
  );

  const handleDelete = React.useCallback(
    async (id: number | null) => {
      if (id) {
        const response = await removeEmployeeLevel(id);

        // Handle the delete API error.
        if (response.error) {
          const message =
            "data" in response.error
              ? resolveApiErrorMessage(response.error.data as string | object)
              : DEFAULT_API_ERROR_MESSAGE;

          toast.error(`Error deleting employee level: ${message}`);
        } else {
          toast.success(`Employee Level Deleted`);
          // Reset form on success.
          setShowDeleteModal(false);
          setTempFormId(null);
        }
      }
    },
    [removeEmployeeLevel]
  );

  return (
    <>
      <div
        className={styles["admin-controls"]}
        aria-description="container to employee level controls"
      >
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          onClick={() => setShowAddModal(true)}
        >
          <FontAwesomeIcon icon={faPlus} />
          Add Employee Level
        </button>
      </div>
      {isLoading ? (
        <div
          className={styles["admin-loading"]}
          aria-description="container to display when loading initial data"
        >
          <MoonLoader />
        </div>
      ) : (
        <div
          className={styles["card-list"]}
          aria-description="container for list of employee levels"
        >
          <ul>
            {(employeeLevels?.data as IEmployeeLevel[]).map((employeeLevel) => {
              return (
                <li key={employeeLevel.id}>
                  <FormCard
                    key={employeeLevel.id}
                    formProps={{
                      formData: {
                        name: employeeLevel.name,
                        level: employeeLevel.level,
                        description: employeeLevel.description,
                      },
                      schema: employeeLevelSchema,
                      uiSchema: employeeLevelUiSchema,
                      validator: validator,
                      widgets: employeeLevelWidgets,
                    }}
                    /**
                     * TODO: Uncomment in PMBIPO-436.
                      onDelete={() => {
                        setTempFormData(null);
                        setTempFormId(employeeLevel.id);
                        setShowDeleteModal(true);
                      }}
                    */
                    onSubmit={(submittedData) => {
                      setTempFormData(submittedData?.formData);
                      setTempFormId(employeeLevel.id);
                      setShowUpdateModal(true);
                    }}
                  />
                </li>
              );
            })}
          </ul>
        </div>
      )}
      <ConfirmModal
        title={"Update Employee Level"}
        open={showUpdateModal}
        acceptLabel={<>Update</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleUpdate(tempFormId, tempFormData)}
        onReject={() => setShowUpdateModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
      <ConfirmModal
        title={"Delete Employee Level"}
        open={showDeleteModal}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleDelete(tempFormId)}
        onReject={() => setShowDeleteModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />

      <ConfirmModal
        title={"Add Employee Level"}
        open={showAddModal}
        acceptLabel={<>Add</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleCreate()}
        onReject={() => handleCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
        className={styles["new-modal-form"]}
      >
        <Form
          key={newFormKey}
          ref={newFormRef}
          validator={validator}
          schema={employeeLevelSchema}
          uiSchema={updatedUiSchema}
          showErrorList={false}
          noHtml5Validate={true}
          widgets={employeeLevelWidgets}
        />
      </ConfirmModal>
    </>
  );
}
