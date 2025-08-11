import React from "react";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { faAdd } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import { Dropdown } from "primereact/dropdown";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";
import FormType from "@rjsf/core";
import { Form } from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import FormCard from "views/components/FormCard/FormCard";

import {
  SubFunctionFormData,
  subFunctionSchema,
  subFunctionUiSchema,
} from "views/schemas/administration/SubFunctionSchema";

import { IFunction } from "definitions/portal/directory/Function.types";
import { ISubFunction } from "definitions/portal/directory/SubFunction.types";

import { useGetFunctionsAdminQuery } from "state/query/api/portal/directory/FunctionApi";
import {
  useAddSubFunctionMutation,
  useGetSubFunctionsQuery,
  useRemoveSubFunctionMutation,
  useUpdateSubFunctionMutation,
} from "state/query/api/portal/directory/SubFunctionApi";

import styles from "views/containers/AdminControls/AdminControls.module.css";

export default function SubFunctions() {
  const { data: functionsData, isLoading: isLoadingFunctions } =
    useGetFunctionsAdminQuery(null);
  const { data: subFunctionsData, isLoading: isLoadingSubFunctions } =
    useGetSubFunctionsQuery(null);

  const [addSubFunction] = useAddSubFunctionMutation();
  const [removeSubFunction] = useRemoveSubFunctionMutation();
  const [updateSubFunction] = useUpdateSubFunctionMutation();

  const [functions, setFunctions] = React.useState<IFunction[]>([]);
  const [subfunctions, setSubFunctions] = React.useState<ISubFunction[]>([]);

  const [selectedFunction, setSelectedFunction] =
    React.useState<IFunction | null>(null);
  const [selectedSubFunction, setSelectedSubFunction] =
    React.useState<ISubFunction | null>(null);

  const newSubFunctionFormRef = React.useRef<FormType>(null);
  const [newSubFunctionFormKey, setNewSubFunctionFormKey] = React.useState(
    Date.now()
  );

  const [showAddModal, setShowAddModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);
  const [showUpdateModal, setShowUpdateModal] = React.useState(false);

  /**
   * Fetch the `SubFunction` and `Function` entries from the
   * database.
   */
  React.useEffect(() => {
    setSubFunctions(
      lodash.cloneDeep((subFunctionsData?.data as ISubFunction[]) ?? [])
    );
    setFunctions(lodash.cloneDeep((functionsData?.data as IFunction[]) ?? []));
  }, [functionsData, subFunctionsData, setFunctions, setSubFunctions]);

  const updatedUiSchema = React.useMemo(() => {
    if (subfunctions && functions) {
      return {
        ...subFunctionUiSchema,
        function: {
          ...subFunctionUiSchema?.function,
          "ui:options": {
            functions: functions,
          },
        },
        "ui:submitButtonOptions": {
          norender: true,
        },
      };
    }
  }, [subfunctions, functions]);

  const updatedSchema = React.useMemo(() => {
    if (functions) {
      return {
        ...subFunctionSchema,
        properties: {
          ...subFunctionSchema.properties,
          function: {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            ...(subFunctionSchema?.properties as any)?.function,
            oneOf: functions.map((functionEntry) => ({
              const: functionEntry.id,
              title: functionEntry.name,
            })),
          },
        },
      };
    }
  }, [functions]);

  const handleDeleteSubFunction = React.useCallback(async () => {
    if (selectedSubFunction) {
      removeSubFunction(selectedSubFunction?.id)
        .unwrap()
        .then(() => toast.success("Successfully deleted SubFunction."))
        .catch((error: FetchBaseQueryError) =>
          toast.error(error?.data as string)
        );
    }
    setSelectedSubFunction(null);
    setShowDeleteModal(false);
  }, [selectedSubFunction, removeSubFunction]);

  const handleUpdateSubFunction = React.useCallback(async () => {
    if (selectedSubFunction) {
      updateSubFunction({
        body: {
          name: selectedSubFunction.name,
          description: selectedSubFunction.description,
          function: selectedSubFunction.function as unknown as number,
        },
        id: selectedSubFunction.id,
      })
        .unwrap()
        .then(() => toast.success("Successfully updated SubFunction."))
        .catch((error: FetchBaseQueryError) =>
          toast.error(error?.data as string)
        );

      setShowUpdateModal(false);
      setSelectedSubFunction(null);
    }
  }, [
    selectedSubFunction,
    setSelectedSubFunction,
    setShowUpdateModal,
    updateSubFunction,
  ]);

  const handleUpdateModalCancel = React.useCallback(() => {
    setSelectedSubFunction(null);
    setShowUpdateModal(false);
  }, [setSelectedSubFunction, setShowUpdateModal]);

  const handleAddSubFunction = React.useCallback(async () => {
    if (
      newSubFunctionFormRef?.current &&
      newSubFunctionFormRef?.current?.validateForm()
    ) {
      const newSubFunctionFormData: SubFunctionFormData = {
        ...newSubFunctionFormRef?.current?.state?.formData,
      };

      addSubFunction({
        ...newSubFunctionFormData,
      })
        .unwrap()
        .then(() => toast.success("Successfully added SubFunction."))
        .catch((error: FetchBaseQueryError) =>
          toast.error(error?.data as string)
        );

      setShowAddModal(false);
      setNewSubFunctionFormKey(Date.now());
    }
  }, [addSubFunction, setNewSubFunctionFormKey, setShowAddModal]);

  const handleAddModalCancel = React.useCallback(() => {
    setShowAddModal(false);
    setNewSubFunctionFormKey(Date.now());
  }, [setShowAddModal, setNewSubFunctionFormKey]);

  if (isLoadingFunctions || isLoadingSubFunctions) {
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
    <>
      <div
        className={styles["admin-controls"]}
        aria-description="container for subfunction controls"
      >
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          onClick={() => setShowAddModal(true)}
        >
          <FontAwesomeIcon icon={faAdd} /> Add Subfunction
        </button>
        <Dropdown
          className={styles["admin-dropdown-filter"]}
          options={functions}
          value={selectedFunction}
          onChange={(e) => setSelectedFunction(e?.value)}
          optionLabel="name"
          placeholder="Filter by Function"
          showClear
        />
      </div>
      <div
        className={styles["card-list"]}
        aria-description="container for list of subfunctions"
      >
        <ul>
          {updatedSchema &&
            updatedUiSchema &&
            subfunctions
              ?.filter((subFunction) =>
                selectedFunction
                  ? subFunction?.function?.id === selectedFunction?.id
                  : subFunction
              )
              .map((subFunction, index) => (
                <li key={`${index}-${subFunction?.id}`}>
                  <FormCard
                    formProps={{
                      schema: updatedSchema,
                      uiSchema: updatedUiSchema,
                      formData: {
                        name: subFunction.name,
                        description: subFunction.description,
                        function: subFunction.function.id,
                      },
                      validator: validator,
                    }}
                    /**
                     * TODO: Uncomment in PMBIPO-436.
                    onDelete={() => {
                      setSelectedSubFunction({ ...subFunction });
                      setShowDeleteModal(true);
                    }}
                    */
                    onSubmit={(e) => {
                      setSelectedSubFunction({
                        ...subFunction,
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
        title="Add SubFunction"
        open={showAddModal}
        className={styles["new-modal-form"]}
        acceptLabel={<>Add</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleAddSubFunction()}
        onReject={() => handleAddModalCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      >
        {updatedSchema && updatedUiSchema && (
          <Form
            key={newSubFunctionFormKey}
            ref={newSubFunctionFormRef}
            schema={updatedSchema}
            uiSchema={updatedUiSchema}
            validator={validator}
            showErrorList={false}
            noHtml5Validate={true}
          />
        )}
      </ConfirmModal>
      <ConfirmModal
        title="Update SubFunction"
        open={showUpdateModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Update</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleUpdateSubFunction()}
        onReject={() => handleUpdateModalCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
      <ConfirmModal
        title="Delete SubFunction"
        open={showDeleteModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleDeleteSubFunction()}
        onReject={() => setShowDeleteModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
    </>
  );
}
