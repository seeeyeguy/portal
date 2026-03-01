import React from "react";
import { useLoaderData } from "react-router";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import { faFilter, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import { Dropdown, DropdownChangeEvent } from "primereact/dropdown";
import { MultiSelect, MultiSelectChangeEvent } from "primereact/multiselect";
import { Paginator, PaginatorPageChangeEvent } from "primereact/paginator";
import { Checkbox } from "primereact/checkbox";
import FormType from "@rjsf/core";
import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import ResourceRequestAccordion from "views/components/ResourceRequestAccordion/ResourceRequestAccordion";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";
import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";
import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { IAuthUser } from "definitions/Sso.types";

import { searchForEmployees } from "services/auth/ldapService";
import { useGetEmployeeLevelsAdminQuery } from "state/query/api/portal/directory/EmployeeLevelApi";
import { useGetSubFunctionsQuery } from "state/query/api/portal/directory/SubFunctionApi";
import { useGetTagsQuery } from "state/query/api/portal/directory/TagApi";
import {
  useAddRequestMutation,
  useGetRequestsQuery,
  useUpdateRequestMutation,
  useRemoveRequestMutation,
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

import { hasSuperuserPermissions } from "utils/PermissionUtility";
import { debounce, resolveApiErrorMessage } from "utils/PromiseUtility";
import { base64ImageToFile } from "views/utils/ImageUtility";
import {
  getThumbnailPath,
  resourceTypeThumbnailPaths,
} from "views/utils/ResourceLinksUtility";
import { tooltipTemplate } from "views/utils/RequestUtility";

import styles from "views/containers/AdminControls/AdminControls.module.css";
import { useRefreshRequestNotificationsMutation } from "state/query/api/portal/request/RequestNotificationApi";

const EDITABLE_STAGES = [1, 4];
const REVISABLE_STAGES = [99];

const DRAFT = "DRAFT";
const SUBMITTED = "SUBMITTED";

export default function AdminResources() {
  const loaderData = useLoaderData() as { user: IAuthUser };

  const superuserPermissions = React.useMemo(
    () => hasSuperuserPermissions(loaderData.user),
    [loaderData]
  );

  // Filter State.
  const [selectedFilters, setSelectedFilters] = React.useState<
    (string | number)[]
  >([]);

  const [showDeleted, setShowDeleted] = React.useState(false);

  // Multi-Select filter options, non-superusers get their resources
  // filtered by default so the first option is removed.
  const filterOptions = React.useMemo(
    () =>
      selectedFilters.includes(0)
        ? [
            { name: "My Resources", value: 0 },
            { name: "Drafts/Revisions", value: 1 },
            { name: "Pending", value: "PENDING" },
            { name: "Approved", value: "APPROVED" },
            { name: "Rejected", value: "REJECTED" },
          ].filter(Boolean)
        : [{ name: "My Resources", value: 0 }],
    [selectedFilters]
  );

  // Pagination State.
  const [page, setPage] = React.useState(0);
  const [first, setFirst] = React.useState(0);
  const [rows, setRows] = React.useState(5);
  const [totalRows, setTotalRows] = React.useState(rows);

  // Pagination State Updates.
  const onPageChange = (event: PaginatorPageChangeEvent) => {
    setPage(event.page);
    setFirst(event.first + 1);
    setRows(event.rows);
  };

  // Filter State Updates.
  const handleFilterChange = (event: MultiSelectChangeEvent) => {
    const selectedValues: (number | string)[] = event.value;

    // Ensure "My Resources" can coexist with any other value.
    const myResourcesSelected = selectedValues.some((filter) => filter === 0);

    // Early return when "My Resources" is not selected with all other filters removed.
    if (!myResourcesSelected) {
      setSelectedFilters([]);
      setTotalRows(rows);
      return;
    }

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

  const [selectedSubFunction, setSelectedSubFunction] = React.useState<
    number[]
  >([]);

  const handleSubFunctionChange = (event: DropdownChangeEvent) => {
    const selectedValues: number[] = event.value ? [event.value] : [];
    setSelectedSubFunction(selectedValues);
    setTotalRows(rows);
  };

  const usersPermittedSubFunctions = React.useMemo(
    () =>
      Array.from(
        loaderData.user.accesses?.reduce((acc, access) => {
          access.subfunctions.forEach((id) => {
            if (!superuserPermissions) {
              acc.add(id);
            }
          });
          return acc;
        }, new Set<number>())
      ),
    [loaderData, superuserPermissions]
  );

  // Queries.
  const {
    data: requests,
    isLoading,
    isFetching,
  } = useGetRequestsQuery({
    originator:
      // Filter to user requests if they have the filter or if they are not a superuser.
      selectedFilters.includes(0) ? loaderData.user.username : null,
    // If "My Resources" is selected, filter request status by string value in selected filters, else only show APPROVED resources.
    status: selectedFilters.includes(0)
      ? ((selectedFilters.find((filter) =>
          lodash.isString(filter)
        ) as string) ?? null)
      : "APPROVED",
    // Filter request stage by number value in selected filters.
    stages: selectedFilters.reduce((acc, filter) => {
      if (lodash.isNumber(filter) && filter > 0 && !acc.length) {
        return [...acc, filter];
      }
      return acc;
    }, [] as number[]),
    subfunctions: selectedSubFunction ?? usersPermittedSubFunctions,
    page: page + 1,
    limit: rows,
    deleted: showDeleted
  });
  
  // Adjust pagination pages after data load.
  React.useEffect(() => {
    const currentRows = (requests?.data.length ?? 0) * (first / rows + 1) + 1;
    if (currentRows) {
      setTotalRows((prevRows) => Math.max(prevRows, currentRows));
    } else {
      // prevents excessive paging past the last page of resources.
      setTotalRows(first);
    }
  }, [requests?.data, first, page, rows]);

  const [updateResource] = useUpdateRequestMutation();

  const [addResource] = useAddRequestMutation();

  const [removeRequest] = useRemoveRequestMutation();

  const [refreshRequestNotifications] =
    useRefreshRequestNotificationsMutation();

  const { data: tags } = useGetTagsQuery(null);
  const { data: employeeLevels, isLoading: isEmployeeLevelsLoading } =
    useGetEmployeeLevelsAdminQuery(null);
  const { data: subfunctions, isLoading: isSubfunctionsLoading } =
    useGetSubFunctionsQuery(null);
  const resourceTypes = Object.keys(resourceTypeThumbnailPaths);

  const filterSubfunctionOptions = React.useMemo(
    () =>
      ((subfunctions?.data ?? []) as ISubFunction[]).reduce(
        (acc, record) => {
          if (
            !superuserPermissions &&
            !usersPermittedSubFunctions.includes(record.id)
          ) {
            return acc;
          }
          return [
            ...acc,
            {
              name: `${record.name} (${record.function.name})`,
              value: record.id,
            },
          ];
        },
        [] as { name: string; value: number }[]
      ),
    [subfunctions, superuserPermissions, usersPermittedSubFunctions]
  );

  const fetchUserOptions = React.useCallback(
    async (
      searchTerm: string,
      secondaryPreviousPoc?: string
    ): Promise<string[]> => {
      if (!searchTerm?.length) {
        return [];
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
        return (data?.data ?? []).map(
          (employee) => `${prefix}${employee.email}`
        );
      } else {
        return (data?.data ?? []).map((employee) => employee.email);
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
        primaryPoc: {
          ...resourceUiSchema.primaryPoc,
          "ui:options": {
            completeMethod: (searchTerm: string) => {
              return debouncedFetchPoc(searchTerm);
            },
          },
        },
        secondaryPoc: {
          ...resourceUiSchema.secondaryPoc,
          "ui:options": {
            completeMethod: (searchTerm: string) => {
              return debouncedFetchPoc(
                searchTerm.includes(",")
                  ? searchTerm.split(",").pop()!.trim()
                  : searchTerm,
                searchTerm
              );
            },
          },
        },
        "ui:submitButtonOptions": {
          norender: true,
        },
      };
    }
    return resourceUiSchema;
  }, [tags, debouncedFetchPoc]);

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
    (newSchema.properties?.type as any).oneOf = resourceTypes.map((type) => ({
      const: type,
      title: type,
    }));

    return newSchema;
  }, [employeeLevels, subfunctions, resourceTypes]);

  React.useEffect(() => {
    setNewFormKey(Date.now());
  }, [isEmployeeLevelsLoading, isSubfunctionsLoading]);

  const formRefs = React.useRef(new Map());
  const [formKeys, setFormKeys] = React.useState(new Map());

  const newFormRef = React.useRef<FormType>(null);
  const [newFormKey, setNewFormKey] = React.useState(Date.now());

  const [showNewModal, setShowNewModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState<number | null>(null);

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
              ? resolveApiErrorMessage(response.error.data as string | object)
              : DEFAULT_API_ERROR_MESSAGE;

          console.error(message);
          toast.error(`Error Saving Request: ${message}`);
        } else {
          toast.success("Request Updated");
          refreshRequestNotifications();
        }
      }
    },
    [refreshRequestNotifications, updateResource]
  );

const handleCreate = React.useCallback(
  async (
    stage: "DRAFT" | "SUBMITTED",
    uid?: string,
    previousRevision?: number,
    requestId?: number,
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
            ? resolveApiErrorMessage(response.error.data as string | object)
            : DEFAULT_API_ERROR_MESSAGE;

        console.error(message);
        toast.error(`Error Saving Request: ${message}`);
      } else {
        toast.success("Request Created");
        refreshRequestNotifications();
        // Reset form on success.
        setShowNewModal(false);
        setNewFormKey(Date.now());
      }
    }
  },
  [addResource, refreshRequestNotifications]
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
          disabled={isEmployeeLevelsLoading || isSubfunctionsLoading}
          onClick={() => setShowNewModal(true)}
        >
          <FontAwesomeIcon icon={faPlus} />
          Add Resource
        </button>
        <Paginator
          className={styles["admin-paginator"]}
          first={first}
          rows={rows}
          totalRecords={totalRows}
          rowsPerPageOptions={[5, 10, 20]}
          onPageChange={onPageChange}
        />
        <Dropdown
          className={styles["admin-dropdown-filter"]}
          value={selectedSubFunction[0]}
          options={filterSubfunctionOptions}
          optionLabel="name"
          optionValue="value"
          onChange={handleSubFunctionChange}
          placeholder="Filter by SubFunction"
          showClear
        />
        <div className={styles["admin-deleted-checkbox"]}>
          <Checkbox
            inputId="showDeleted"
            checked={showDeleted}
            onChange={(e) => setShowDeleted(!!e.checked)}

          />
          <label htmlFor="showDeleted">Show Deleted</label>
        </div>
        <MultiSelect
          value={selectedFilters}
          onChange={handleFilterChange}
          options={filterOptions}
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
                    tooltipContent={tooltipTemplate(request)}
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
                              Save as Draft
                            </button>
                          {request.status === "APPROVED" && (
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
                              onClick={() => setShowDeleteModal(request.id)}
                              aria-label="delete"
                            >
                              Delete
                            </button>
                          )}
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
        title="Submit Resource Deletion"
        open={!!showDeleteModal}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={async () => {
          const req = requests?.data.find(r => r.id === showDeleteModal);

          try {
            if (!req?.resource?.id) {
              throw new Error("Request resource ID is missing");
            }

            await removeRequest(req.resource.id).unwrap();

            toast.success("Delete Request Submitted");
            refreshRequestNotifications();
            } catch (err: unknown) {
              const apiErr = err as { data?: string | object };
              const errorData: string | object = apiErr.data ?? apiErr;

              toast.error(resolveApiErrorMessage(errorData));
            }

          setShowDeleteModal(null);
        }}
        onReject={() => setShowDeleteModal(null)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      >
      </ConfirmModal>
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
        />
      </ConfirmModal>
    </>
  );
}
