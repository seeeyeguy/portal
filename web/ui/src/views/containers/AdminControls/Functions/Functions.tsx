import React from "react";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { faAdd } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { JSONSchema7 } from "json-schema";
import lodash from "lodash";
import { Dropdown } from "primereact/dropdown";
import FormType from "@rjsf/core";
import { Form } from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import FormCard from "views/components/FormCard/FormCard";

import {
  FunctionFormData,
  functionSchema,
  functionUiSchema,
} from "views/schemas/administration/FunctionSchema";

import { IFunction } from "definitions/portal/directory/Function.types";

import {
  useAddFunctionMutation,
  useGetFunctionsQuery,
  useUpdateFunctionMutation,
  useRemoveFunctionMutation,
} from "state/query/api/portal/directory/FunctionApi";

import styles from "views/containers/AdminControls/AdminControls.module.css";

export default function Functions() {
  const { data: functions, isLoading: isLoadingFunctions } =
    useGetFunctionsQuery(null);

  const [functionsList, setFunctionsList] = React.useState<IFunction[]>([]);

  const [selectedFunction, setSelectedFunction] =
    React.useState<IFunction | null>(null);

  const [addFunction] = useAddFunctionMutation();
  const [updateFunction] = useUpdateFunctionMutation();
  const [deleteFunction] = useRemoveFunctionMutation();

  const newFunctionFormRef = React.useRef<FormType>(null);
  const [newFunctionFormKey, setNewFunctionFormKey] = React.useState(
    Date.now()
  );

  const [showAddModal, setShowAddModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);
  const [showUpdateModal, setShowUpdateModal] = React.useState(false);

  React.useEffect(() => {
    setFunctionsList(lodash.cloneDeep((functions?.data as IFunction[]) ?? []));
  }, [functions]);

  const updatedUiSchema = React.useMemo(() => {
    if (functionsList) {
      return {
        ...functionUiSchema,
        function: {
          ...functionUiSchema?.function,
          "ui:options": {
            functions: functionsList,
          },
        },
        "ui:submitButtonOptions": {
          norender: true,
        },
      };
    }
  }, [functionsList]);

  const updatedSchema = React.useMemo(() => {
    if (functionsList) {
      return {
        ...functionSchema,
        properties: {
          ...functionSchema.properties,
          function: {
            ...(functionSchema?.properties?.function as JSONSchema7),
            oneOf: functionsList.map((functionEntry) => ({
              const: functionEntry.id,
              title: functionEntry.name,
            })),
          },
        },
      };
    }
  }, [functionsList]);

  const handleDeleteFunction = React.useCallback(async () => {
    if (selectedFunction) {
      deleteFunction(selectedFunction.id)
        .unwrap()
        .then(() => toast.success("Successfully deleted Function."))
        .catch((error) => toast.error(error.data));

      setSelectedFunction(null);
      setShowDeleteModal(false);
    }
  }, [
    selectedFunction,
    deleteFunction,
    setSelectedFunction,
    setShowDeleteModal,
  ]);

  const handleUpdateFunction = React.useCallback(async () => {
    if (selectedFunction) {
      updateFunction({
        body: {
          name: selectedFunction.name,
          description: selectedFunction.description,
        },
        id: selectedFunction.id,
      })
        .unwrap()
        .then(() => toast.success("Successfully updated Function."))
        .catch((error) => toast.error(error.data));

      setShowUpdateModal(false);
      setSelectedFunction(null);
    }
  }, [
    selectedFunction,
    setSelectedFunction,
    setShowUpdateModal,
    updateFunction,
  ]);

  const handleUpdateModalCancel = React.useCallback(() => {
    setSelectedFunction(null);
    setShowUpdateModal(false);
  }, [setSelectedFunction, setShowUpdateModal]);

  const handleAddFunction = React.useCallback(async () => {
    if (
      newFunctionFormRef?.current &&
      newFunctionFormRef?.current?.validateForm()
    ) {
      const newFunctionFormData: FunctionFormData = {
        ...newFunctionFormRef?.current?.state?.formData,
      };

      addFunction({
        ...newFunctionFormData,
      })
        .unwrap()
        .then(() => toast.success("Successfully added Function."))
        .catch((error) => toast.error(error.data));

      setShowAddModal(false);
      setNewFunctionFormKey(Date.now());
    }
  }, [addFunction, setNewFunctionFormKey, setShowAddModal]);

  const handleAddModalCancel = React.useCallback(() => {
    setShowAddModal(false);
    setNewFunctionFormKey(Date.now());
  }, [setShowAddModal, setNewFunctionFormKey]);

  if (isLoadingFunctions) {
    return (
      <div
        className={styles["admin-loading"]}
        aria-description="container to display when loading initial data"
      >
        <MoonLoader />
      </div>
    );
  }

  return (
    <section>
      <div
        className={styles["admin-controls"]}
        aria-description="function admin page controls"
      >
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          onClick={() => setShowAddModal(true)}
        >
          <FontAwesomeIcon icon={faAdd} /> Add function
        </button>
        <Dropdown
          options={functionsList}
          value={selectedFunction}
          optionLabel="name"
          placeholder="Select a Function"
          showClear
          filter
          filterBy="name"
          filterMatchMode="contains"
          className={styles["admin-dropdown-filter"]}
          onChange={(e) => setSelectedFunction(e?.value)}
        />
      </div>
      <div
        className={styles["card-list"]}
        aria-description="function list container"
      >
        <ul>
          {updatedSchema &&
            updatedUiSchema &&
            functionsList
              ?.filter((functionEntry) =>
                selectedFunction
                  ? functionEntry?.id === selectedFunction?.id
                  : functionEntry
              )
              .map((functionEntry, index) => (
                <li key={`${index}-${functionEntry?.id}`}>
                  <FormCard
                    formProps={{
                      schema: updatedSchema,
                      uiSchema: updatedUiSchema,
                      formData: {
                        ...functionEntry,
                        function: functionEntry.id,
                      },
                      validator: validator,
                    }}
                    onDelete={() => {
                      setSelectedFunction({ ...functionEntry });
                      setShowDeleteModal(true);
                    }}
                    onSubmit={(e) => {
                      setSelectedFunction({
                        ...functionEntry,
                        ...e?.formData,
                      });
                      setShowUpdateModal(true);
                    }}
                  />
                </li>
              ))}
        </ul>
      </div>

      <ConfirmModal
        title="Add Function"
        open={showAddModal}
        className={styles["new-modal-form"]}
        acceptLabel={<>Add</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleAddFunction()}
        onReject={() => handleAddModalCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      >
        {updatedSchema && updatedUiSchema && (
          <Form
            key={newFunctionFormKey}
            ref={newFunctionFormRef}
            schema={updatedSchema}
            uiSchema={updatedUiSchema}
            validator={validator}
            showErrorList={false}
            noHtml5Validate={true}
          />
        )}
      </ConfirmModal>

      <ConfirmModal
        title="Update Function"
        open={showUpdateModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Update</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleUpdateFunction()}
        onReject={() => handleUpdateModalCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />

      <ConfirmModal
        title="Delete Function"
        open={showDeleteModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleDeleteFunction()}
        onReject={() => setShowDeleteModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
    </section>
  );
}
