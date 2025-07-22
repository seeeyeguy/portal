import React from "react";
import { useLoaderData } from "react-router";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import lodash from "lodash";
import { faFilter, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import FormType from "@rjsf/core";
import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";
import { MultiSelect, MultiSelectChangeEvent } from "primereact/multiselect";
import { Paginator, PaginatorPageChangeEvent } from "primereact/paginator";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import ResourceRequestAccordion from "views/components/ResourceRequestAccordion/ResourceRequestAccordion";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";
import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";
import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { IAuthUser } from "definitions/Sso.types";

import { searchForEmployees } from "services/auth/ldapService";
import { useGetEmployeeLevelsQuery } from "state/query/api/portal/directory/EmployeeLevelApi";
import { useGetSubFunctionsQuery } from "state/query/api/portal/directory/SubFunctionApi";
import { useGetTagsQuery } from "state/query/api/portal/directory/TagApi";
import {
  useAddRequestMutation,
  useGetRequestsQuery,
  useUpdateRequestMutation,
} from "state/query/api/portal/request/RequestApi";
import {
  TApiPostRequestRequest,
  TApiPutRequestRequest,
} from "state/query/api/portal/request/RequestApi";

import {
  resourceCustomValidate,
  ResourceFormData,
  resourceSchema,
  resourceUiSchema,
  resourceWidgets,
  transformResourceToFormData,
} from "views/schemas/administration/ResourceSchema";

import { debounce } from "utils/PromiseUtility";
import { base64ImageToFile } from "views/utils/ImageUtility";
import {
  getThumbnailPath,
  resourceTypeThumbnailPaths,
} from "views/utils/ResourceLinksUtility";
import { tooltipTemplate } from "views/utils/RequestUtility";

import styles from "views/containers/AdminControls/AdminControls.module.css";

const EDITABLE_STAGES = [1, 4];
const REVISABLE_STAGES = [99];

const DRAFT = "DRAFT";
const SUBMITTED = "SUBMITTED";

const ROLE_LEVELS = {
  SUPERUSER: 1,
  BUSINESS_PROCESS_EXPERT: 2,
  DATA_STEWARD: 3,
};

export default function AdminResources() {
  const loaderData = useLoaderData() as { user: IAuthUser };

  const superuserPermissions = React.useMemo(
    () =>
      loaderData.user.accesses?.some(
        (access) => access.role.level == ROLE_LEVELS.SUPERUSER
      ) || loaderData.user.isAdmin,
    [loaderData]
  );

  const [primaryPocSearch, setPrimaryPocSearch] = React.useState<string[]>([]);

  const [secondaryPocSearch, setSecondaryPocSearch] = React.useState<string[]>(
    []
  );

  // Multi-Select filter options, non-superusers get their resources
  // filtered by default so the first option is removed.
  const FILTER_OPTIONS = [
    superuserPermissions && { name: "My Resources", value: 0 },
    { name: "Draft", value: 1 },
    { name: "Revise", value: 4 },
    { name: "Pending", value: "PENDING" },
    { name: "Approved", value: "APPROVED" },
    { name: "Rejected", value: "REJECTED" },
  ].filter(Boolean);

  // Pagination State.
  const [page, setPage] = React.useState(0);
  const [rows, setRows] = React.useState(5);
  const [totalRows, setTotalRows] = React.useState(rows);

  // Pagination State Updates.
  const onPageChange = (event: PaginatorPageChangeEvent) => {
    setPage(event.first);
    setRows(event.rows);
  };

  // Filter State.
  const [selectedFilters, setSelectedFilters] = React.useState<
    (string | number)[]
  >(superuserPermissions ? [0] : []);

  // Filter State Updates.
  const handleFilterChange = (event: MultiSelectChangeEvent) => {
    const selectedValues: (number | string)[] = event.value;

    // Ensure "My Resources" can coexist with any other value.
    const myResourcesSelected = selectedValues.some((filter) => filter === 0);

    // Remove other values if more than one is selected (excluding "My Resources").
    const otherSelectedValues = selectedValues.filter((filter) => filter !== 0);
    if (otherSelectedValues.length > 1) {
      const lastSelectedValue =
        otherSelectedValues[otherSelectedValues.length - 1];
      setSelectedFilters(
        myResourcesSelected ? [0, lastSelectedValue] : [lastSelectedValue]
      );
    } else {
      setSelectedFilters(selectedValues);
    }
    setTotalRows(rows);
  };

  // Queries.
  const {
    data: requests,
    isLoading,
    isFetching,
  } = useGetRequestsQuery({
    originator:
      // Filter to user requests if they have the filter or if they are not a superuser.
      !superuserPermissions || selectedFilters.includes(0)
        ? loaderData.user.email
        : null,
    // Filter request status by string value in selected filters.
    status:
      (selectedFilters.find((filter) => lodash.isString(filter)) as string) ??
      null,
    // Filter request stage by number value in selected filters.
    stage:
      (selectedFilters.find(
        (filter) => lodash.isNumber(filter) && filter > 0
      ) as number) ?? null,
    page: page,
    limit: rows,
  });

  // Adjust pagination pages after data load.
  React.useEffect(() => {
    const currentRows = (requests?.data.length ?? 0) * (page / rows + 1) + 1;
    setTotalRows((prevRows) => Math.max(prevRows, currentRows));
  }, [requests?.data, page, rows]);

  const [updateResource] = useUpdateRequestMutation();

  const [addResource] = useAddRequestMutation();

  const { data: tags } = useGetTagsQuery(null);
  const { data: employeeLevels } = useGetEmployeeLevelsQuery(null);
  const { data: subfunctions } = useGetSubFunctionsQuery(null);
  const resourceTypes = Object.keys(resourceTypeThumbnailPaths);

  const fetchUserOptions = React.useCallback(
    async (searchTerm: string, secondaryPreviousPoc?: string) => {
      if (!searchTerm?.length) {
        setPrimaryPocSearch([]);
        return;
      }

      let data = null;
      try {
        let modifiedSearchTerm = searchTerm;
        if (
          modifiedSearchTerm.includes(".") &&
          modifiedSearchTerm[0] !== "." &&
          !modifiedSearchTerm.includes("@")
        ) {
          const splitSearchTerm = modifiedSearchTerm.split(".");
          const [firstName, ...lastName] = splitSearchTerm;
          modifiedSearchTerm = firstName.trim();
          if (
            splitSearchTerm.length > 1 &&
            lastName?.length &&
            lastName[lastName.length - 1].trim()?.length
          ) {
            modifiedSearchTerm = `${modifiedSearchTerm} ${lastName[lastName.length - 1].trim()}`;
          }
        }
        data = await searchForEmployees(modifiedSearchTerm, 1, 25);
      } catch (err) {
        data = {};
      }
      if (secondaryPreviousPoc) {
        // Extract the part of the poc string up to and including the last comma.
        const prefix = secondaryPreviousPoc.includes(",")
          ? secondaryPreviousPoc.substring(
              0,
              secondaryPreviousPoc.lastIndexOf(",") + 1
            )
          : "";

        setSecondaryPocSearch(
          (data?.data ?? []).map((employee) => `${prefix}${employee.email}`)
        );
      } else {
        setPrimaryPocSearch(
          (data?.data ?? []).map((employee) => employee.email)
        );
      }
    },
    []
  );

  const debouncedFetchPoc = React.useMemo(
    () => debounce(fetchUserOptions, 300),
    [fetchUserOptions]
  );

  // Schema Options.
  const updatedUiSchema = React.useMemo(() => {
    if (tags) {
      return {
        ...resourceUiSchema,
        tags: {
          ...resourceUiSchema.tags,
          "ui:options": { tags: tags.data },
        },
        "ui:submitButtonOptions": {
          norender: true,
        },
      };
    }
    return resourceUiSchema;
  }, [tags]);

  const updatedSchema = React.useMemo(() => {
    const newSchema = { ...resourceSchema };

    if (employeeLevels) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (newSchema.properties?.employeeLevels as any).items.anyOf = (
        employeeLevels.data as IEmployeeLevel[]
      ).map((level) => ({
        const: level.id,
        title: level.name,
      }));
    }

    if (subfunctions) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (newSchema.properties?.subfunctions as any).items.anyOf = (
        subfunctions.data as ISubFunction[]
      ).map((subFunction) => ({
        const: subFunction.id,
        title: `${subFunction.name} (${subFunction.function.name})`,
      }));
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (newSchema.properties?.primaryPoc as any).examples = primaryPocSearch;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (newSchema.properties?.secondaryPoc as any).examples = secondaryPocSearch;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (newSchema.properties?.type as any).oneOf = resourceTypes.map((type) => ({
      const: type,
      title: type,
    }));

    return newSchema;
  }, [employeeLevels, primaryPocSearch, secondaryPocSearch, subfunctions, resourceTypes]);

  const formRefs = React.useRef(new Map());
  const [formKeys, setFormKeys] = React.useState(new Map());

  const newFormRef = React.useRef<FormType>(null);
  const [newFormKey, setNewFormKey] = React.useState(Date.now());

  const [showNewModal, setShowNewModal] = React.useState(false);

  const handleEdit = React.useCallback(
    async (id: number, stage: "DRAFT" | "SUBMITTED") => {
      const formRef = formRefs.current.get(id);
      if (formRef && formRef.validateForm()) {
        const formSubmission: ResourceFormData = { ...formRef.state.formData };

        // Create request body.
        const body: TApiPutRequestRequest = {
          ...formSubmission,
          // merge all POCs into one array.
          pointOfContacts: [
            formSubmission.primaryPoc,
            ...(formSubmission.secondaryPoc
              ? formSubmission.secondaryPoc
                  .split(",")
                  .map((item) => item.trim())
              : []),
          ],
          thumbnail: base64ImageToFile(formSubmission.thumbnail as string),
          stage,
        };

        const response = await updateResource({ body, id });

        // Handle the updateRequest API error.
        if (response.error) {
          const message =
            "data" in response.error
              ? JSON.stringify(response.error.data)
              : DEFAULT_API_ERROR_MESSAGE;

          console.error(message);
          toast.error(`Error Saving Request: ${JSON.parse(message)}`);
        } else {
          toast.success("Request Updated");
        }
      }
    },
    [updateResource]
  );

  const handleCreate = React.useCallback(
    async (
      stage: "DRAFT" | "SUBMITTED",
      uid?: string,
      previousRevision?: number,
      requestId?: number
    ) => {
      // For revisions we use an existing request form.
      const formRef = requestId
        ? formRefs.current.get(requestId)
        : newFormRef.current;

      if (formRef && formRef.validateForm()) {
        const formSubmission: ResourceFormData = {
          ...formRef.state.formData,
        };

        // Create request body.
        const body: TApiPostRequestRequest = {
          ...formSubmission,
          // merge all POCs into one array.
          pointOfContacts: [
            formSubmission.primaryPoc,
            ...(formSubmission.secondaryPoc
              ? formSubmission.secondaryPoc
                  .split(",")
                  .map((item) => item.trim())
              : []),
          ],
          thumbnail: base64ImageToFile(formSubmission.thumbnail as string),
          stage,
          uid: uid ?? null,
          previousRevision: previousRevision ?? null,
        };

        const response = await addResource(body);

        // Handle the createRequest API error.
        if (response.error) {
          const message =
            "data" in response.error
              ? JSON.stringify(response.error.data)
              : DEFAULT_API_ERROR_MESSAGE;

          console.error(message);
          toast.error(`Error Saving Request: ${JSON.parse(message)}`);
        } else {
          toast.success("Request Created");
          // Reset form on success.
          setShowNewModal(false);
          setNewFormKey(Date.now());
        }
      }
    },
    [addResource]
  );

  // Reset existing resource form back its original data.
  const handleReset = React.useCallback(
    (id: number) => {
      const formRef = formRefs.current.get(id);
      if (formRef) {
        setFormKeys(new Map(formKeys.set(id, `${id}-${Date.now()}`)));
      }
    },
    [formKeys]
  );

  // Clear resource form to empty.
  const handleCancel = React.useCallback(() => {
    setShowNewModal(false);
    setNewFormKey(Date.now());
  }, []);

  return (
    <>
      <div
        className={styles["admin-controls"]}
        aria-description="container to resource controls"
      >
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          onClick={() => setShowNewModal(true)}
        >
          <FontAwesomeIcon icon={faPlus} />
          Add Resource
        </button>
        <Paginator
          className={styles["admin-paginator"]}
          first={page}
          rows={rows}
          totalRecords={totalRows}
          rowsPerPageOptions={[5, 10, 20]}
          onPageChange={onPageChange}
        />
        <MultiSelect
          value={selectedFilters}
          onChange={handleFilterChange}
          options={FILTER_OPTIONS}
          optionLabel="name"
          display="chip"
          placeholder=""
          maxSelectedLabels={2}
          className={styles["admin-filter"]}
          showSelectAll={false}
          panelHeaderTemplate={<></>}
          dropdownIcon={<FontAwesomeIcon icon={faFilter} />}
          data-tooltip-id="filter-tooltip"
          data-tooltip-delay-show={500}
        />
        <Tooltip id="filter-tooltip" place={"left-start"}>
          Filter Resources
        </Tooltip>
        {isFetching && (
          <div
            className={styles["admin-filter-loading"]}
            aria-description="container to display when loading data with filters"
          >
            <MoonLoader size={30} />
          </div>
        )}
      </div>
      {isLoading ? (
        <div
          className={styles["admin-loading"]}
          aria-description="container to display when loading initial data"
        >
          <MoonLoader />
        </div>
      ) : !isFetching && requests?.data.length === 0 ? (
        <p className={styles["admin-loading"]}>No Resources Found</p>
      ) : (
        <div
          className={styles["card-list"]}
          aria-description="container for list of resource requests"
        >
          <ul>
            {requests?.data.map((request) => {
              if (!formKeys.has(request.id)) {
                setFormKeys(
                  new Map(
                    formKeys.set(request.id, `${request.id}-${Date.now()}`)
                  )
                );
              }

              return (
                <li key={request.id}>
                  <ResourceRequestAccordion
                    key={request.id}
                    request={request}
                    thumbnailPath={getThumbnailPath(request.resource)}
                    tooltipContent={tooltipTemplate(request.transitions)}
                    locked={
                      REVISABLE_STAGES.includes(
                        request.transitions.nodes[request.transitions.latest]
                          .stage.level
                      )
                        ? null
                        : !EDITABLE_STAGES.includes(
                            request.transitions.nodes[
                              request.transitions.latest
                            ].stage.level
                          )
                    }
                  >
                    {() => (
                      <div aria-description="container for a resource request">
                        <Form
                          disabled={
                            !EDITABLE_STAGES.includes(
                              request.transitions.nodes[
                                request.transitions.latest
                              ].stage.level
                            ) &&
                            !REVISABLE_STAGES.includes(
                              request.transitions.nodes[
                                request.transitions.latest
                              ].stage.level
                            )
                          }
                          key={formKeys.get(request.id)}
                          ref={(ref) => formRefs.current.set(request.id, ref)}
                          formData={transformResourceToFormData(
                            request.resource
                          )}
                          validator={validator}
                          customValidate={resourceCustomValidate}
                          schema={updatedSchema}
                          uiSchema={updatedUiSchema}
                          showErrorList={false}
                          noHtml5Validate={true}
                          widgets={resourceWidgets}
                          onChange={(event) => {
                            debouncedFetchPoc(event.formData.primaryPoc);
                            // Only search on the last Poc in the list.
                            if (event.formData.secondaryPoc) {
                              debouncedFetchPoc(
                                event.formData.secondaryPoc.includes(",")
                                  ? event.formData.secondaryPoc
                                      .split(",")
                                      .pop()!
                                      .trim()
                                  : event.formData.secondaryPoc,
                                event.formData.secondaryPoc
                              );
                            }
                          }}
                        />
                        {EDITABLE_STAGES.includes(
                          request.transitions.nodes[request.transitions.latest]
                            .stage.level
                        ) && (
                          <div
                            className={styles["button-container"]}
                            aria-description="container for button components"
                          >
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
                              onClick={() => handleReset(request.id)}
                              aria-label="cancel resource edits"
                            >
                              Cancel Edits
                            </button>
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
                              onClick={() => handleEdit(request.id, DRAFT)}
                              aria-label="save resource edit"
                            >
                              Save Draft
                            </button>
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
                              onClick={() => handleEdit(request.id, SUBMITTED)}
                              aria-label="submit resource"
                            >
                              Submit Request
                            </button>
                          </div>
                        )}
                        {REVISABLE_STAGES.includes(
                          request.transitions.nodes[request.transitions.latest]
                            .stage.level
                        ) && (
                          <div
                            className={styles["button-container"]}
                            aria-description="container for button components"
                          >
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
                              onClick={() => handleReset(request.id)}
                              aria-label="cancel Revision edits"
                            >
                              Cancel Revision
                            </button>
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
                              onClick={() =>
                                handleCreate(
                                  DRAFT,
                                  request.resource.uid,
                                  request.resource.id,
                                  request.id
                                )
                              }
                              aria-label="save Revision edit"
                            >
                              Save Revision
                            </button>
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
                              onClick={() =>
                                handleCreate(
                                  SUBMITTED,
                                  request.resource.uid,
                                  request.resource.id,
                                  request.id
                                )
                              }
                              aria-label="submit Revision"
                            >
                              Submit Revision
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </ResourceRequestAccordion>
                </li>
              );
            })}
          </ul>
        </div>
      )}
      <ConfirmModal
        title={"Add Resource"}
        open={showNewModal}
        acceptLabel={<>Request Approval</>}
        alternativeLabel={<>Save Draft</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleCreate(SUBMITTED)}
        onAlternative={() => handleCreate(DRAFT)}
        onReject={() => handleCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
        alternativeClassName={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
        className={styles["new-modal-form"]}
      >
        <Form
          key={newFormKey}
          ref={newFormRef}
          validator={validator}
          customValidate={resourceCustomValidate}
          schema={updatedSchema}
          uiSchema={updatedUiSchema}
          showErrorList={false}
          noHtml5Validate={true}
          widgets={resourceWidgets}
          onChange={(event) => {
            debouncedFetchPoc(event.formData.primaryPoc);
            // Only search on the last Poc in the list.
            if (event.formData.secondaryPoc) {
              debouncedFetchPoc(
                event.formData.secondaryPoc.includes(",")
                  ? event.formData.secondaryPoc.split(",").pop()!.trim()
                  : event.formData.secondaryPoc,
                event.formData.secondaryPoc
              );
            }
          }}
        />
      </ConfirmModal>
    </>
  );
}
