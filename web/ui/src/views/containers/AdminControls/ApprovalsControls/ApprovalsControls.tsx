import React from "react";
import { useLoaderData } from "react-router";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import { faFilter } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import { FloatLabel } from "primereact/floatlabel";
import { InputTextarea } from "primereact/inputtextarea";
import { MultiSelect, MultiSelectChangeEvent } from "primereact/multiselect";
import { Paginator, PaginatorPageChangeEvent } from "primereact/paginator";
import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import ResourceRequestAccordion from "views/components/ResourceRequestAccordion/ResourceRequestAccordion";

import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";
import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { IAccess } from "definitions/portal/users/Access.types";
import { IAuthUser } from "definitions/Sso.types";

import { useGetEmployeeLevelsAdminQuery } from "state/query/api/portal/directory/EmployeeLevelApi";
import { useGetSubFunctionsQuery } from "state/query/api/portal/directory/SubFunctionApi";
import { useGetTagsQuery } from "state/query/api/portal/directory/TagApi";
import {
  useSendDispositionMutation,
  useSubscribeToDispositionQuery,
} from "state/query/api/portal/request/DispositionApi";
import { useGetRequestsQuery } from "state/query/api/portal/request/RequestApi";
import { useGetAccessesQuery } from "state/query/api/portal/users/AccessApi";

import {
  resourceCustomValidate,
  resourceSchema,
  resourceUiSchema,
  resourceWidgets,
  transformResourceToFormData,
} from "views/schemas/administration/ResourceSchema";

import { hasSuperuserPermissions } from "utils/PermissionUtility";
import {
  getThumbnailPath,
  resourceTypeThumbnailPaths,
} from "views/utils/ResourceLinksUtility";
import { tooltipTemplate } from "views/utils/RequestUtility";

import styles from "views/containers/AdminControls/AdminControls.module.css";
import { useRefreshRequestNotificationsMutation } from "state/query/api/portal/request/RequestNotificationApi";

type TDispositionValues = "APPROVED" | "REJECTED" | "REVISE";

const DISPOSITION_VALUES: {
  [key: string]: TDispositionValues;
} = {
  APPROVED: "APPROVED",
  REJECTED: "REJECTED",
  REVISE: "REVISE",
};

const QUERY_REQUEST_PARAMS = {
  id: null,
  originator: null,
  stages: null,
  subfunctions: null,
  status: null,
  page: null,
  limit: null,
  includeArchived: null,
};

const QUERY_USER_ACCESS_PARAMS = {
  id: null,
  user: null,
  roleLevels: null,
  subfunctions: null,
  includeRevoked: null,
};

const REQUEST_STATUSES = {
  PENDING: "PENDING",
  APPROVED: "APPROVED",
  REJECTED: "REJECTED",
};

const STAGE_LEVELS = {
  DRAFT: 1,
  SUBMITTED: 2,
  "APPROVED BY BUSINESS PROCESS OWNER": 3,
  REVISE: 4,
  "REJECTED BY BUSINESS PROCESS OWNER": 5,
  "APPROVED BY SUPERUSER": 99,
  "REJECTED BY SUPERUSER": 100,
};

export default function ApprovalsControls() {
  const loaderData = useLoaderData() as { user: IAuthUser };

  const superuserPermissions = React.useMemo(
    () => hasSuperuserPermissions(loaderData.user),
    [loaderData]
  );

  const usersPermittedStages = React.useMemo(
    () =>
      Array.from(
        loaderData.user.accesses?.reduce((acc, access) => {
          access.stages.forEach((level) => {
            acc.add(level);
          });
          return acc;
        }, new Set<number>())
      ),
    [loaderData]
  );

  const FILTER_STAGES_OPTIONS = React.useMemo(
    () =>
      Object.entries(STAGE_LEVELS).reduce(
        (acc, [key, value]) => {
          if (!usersPermittedStages.includes(value)) {
            return acc;
          }
          return [
            ...acc,
            {
              name: key,
              value,
            },
          ];
        },
        [] as { name: string; value: number }[]
      ),
    [usersPermittedStages]
  );

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

  const { data: accessQuery, isLoading: isLoadingAccesses } =
    useGetAccessesQuery({
      ...QUERY_USER_ACCESS_PARAMS,
    });

  const accesses = React.useMemo(
    () => (accessQuery?.data ?? []) as IAccess[],
    [accessQuery]
  );

  const FILTER_ACCESS_OPTIONS = React.useMemo(
    () =>
      lodash.sortBy(
        accesses.map((access) => ({
          name: `${access.user.firstName} ${access.user.lastName} (${access.user.email})`,
          value: access.user.email.toLowerCase(),
        })),
        ["value"]
      ),
    [accesses]
  );

  const { data: tags } = useGetTagsQuery(null);
  const { data: employeeLevels } = useGetEmployeeLevelsAdminQuery(null);
  const { data: subfunctions } = useGetSubFunctionsQuery(null);

  const FILTER_SUBFUNCTION_OPTIONS = React.useMemo(
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
        [] as unknown as { name: string; value: number }[]
      ),
    [subfunctions, superuserPermissions, usersPermittedSubFunctions]
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

  // Filter State.
  const [selectedAccessFilters, setSelectedAccessFilters] = React.useState<
    string[]
  >([]);
  const [selectedStageFilters, setSelectedStageFilters] = React.useState<
    number[]
  >([]);
  const [selectedSubFunctionFilters, setSelectedSubFunctionFilters] =
    React.useState<number[]>([]);

  // Filter State Updates.
  const handleAccessFilterChange = (event: MultiSelectChangeEvent) => {
    const selectedValues: string[] = event.value;
    // Restrict filters to exactly one selection.
    setSelectedAccessFilters(selectedValues.slice(-1));
    setTotalRows(rows);
  };

  // Filter State Updates.
  const handleSubFunctionFilterChange = (event: MultiSelectChangeEvent) => {
    const selectedValues: number[] = event.value;
    setSelectedSubFunctionFilters(selectedValues);
    setTotalRows(rows);
  };

  // Filter State Updates.
  const handleStageFilterChange = (event: MultiSelectChangeEvent) => {
    const selectedValues: number[] = event.value;
    setSelectedStageFilters(selectedValues);
    setTotalRows(rows);
  };

  const resourceTypes = Object.keys(resourceTypeThumbnailPaths);

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
    (newSchema.properties?.type as any).oneOf = resourceTypes.map((type) => ({
      const: type,
      title: type,
    }));

    return newSchema;
  }, [employeeLevels, subfunctions, resourceTypes]);

  const formRefs = React.useRef(new Map());
  const [formKeys, setFormKeys] = React.useState(new Map());

  // Queries.
  const {
    data: requests,
    isLoading: isLoadingRequests,
    isFetching: isFetchingRequests,
    refetch,
  } = useGetRequestsQuery({
    ...QUERY_REQUEST_PARAMS,
    originator: selectedAccessFilters?.length
      ? selectedAccessFilters[0].replace(/@l3harris.com/i, "@harris.com")
      : null,
    stages: selectedStageFilters?.length
      ? selectedStageFilters
      : usersPermittedStages,
    subfunctions: selectedSubFunctionFilters?.length
      ? selectedSubFunctionFilters
      : usersPermittedSubFunctions,
    status: REQUEST_STATUSES.PENDING,
    page: page + 1,
    limit: rows,
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

  React.useEffect(() => {
    refetch();
  }, [refetch]);

  const [requestId, setRequestId] = React.useState<number | null>(null);
  const [showConfirmModal, setShowConfirmModal] =
    React.useState<boolean>(false);
  const [disposition, setDisposition] = React.useState<TDispositionValues | "">(
    ""
  );
  const [justification, setJustification] = React.useState<string>("");

  const [refreshRequestNotifications] =
    useRefreshRequestNotificationsMutation();
  const [sendDisposition] = useSendDispositionMutation();
  useSubscribeToDispositionQuery({
    ...QUERY_REQUEST_PARAMS,
    originator: selectedAccessFilters?.length
      ? selectedAccessFilters[0].replace(/@l3harris.com/i, "@harris.com")
      : null,
    stages: selectedStageFilters?.length
      ? selectedStageFilters
      : usersPermittedStages,
    subfunctions: selectedSubFunctionFilters?.length
      ? selectedSubFunctionFilters
      : usersPermittedSubFunctions,
    status: REQUEST_STATUSES.PENDING,
    page: page,
    limit: rows,
    deleted: true
  } as unknown as void);

  const confirmDispositionButtonLabel = React.useMemo(() => {
    if (disposition === DISPOSITION_VALUES.REJECTED) {
      return "Reject";
    }

    if (disposition === DISPOSITION_VALUES.REVISE) {
      return "Revise";
    }

    return "Approve";
  }, [disposition]);

  const confirmDispositionButtonStyle = React.useMemo(() => {
    if (disposition === DISPOSITION_VALUES.REJECTED) {
      return styles["admin-button-delete"];
    }

    if (disposition === DISPOSITION_VALUES.REVISE) {
      return styles["admin-button-revise"];
    }

    return styles["admin-button-submit"];
  }, [disposition]);

  const justificationDisabled = React.useMemo(
    () => disposition === DISPOSITION_VALUES.APPROVED || disposition === "",
    [disposition]
  );

  const handleDisposition = React.useCallback(
    (requestId: number, value: TDispositionValues) =>
      (event: React.MouseEvent) => {
        event.preventDefault();
        setRequestId(requestId);
        setDisposition(value);
        setJustification("");
        setShowConfirmModal(true);
      },
    [setDisposition, setJustification, setRequestId, setShowConfirmModal]
  );

  const handleConfirmDisposition = React.useCallback(() => {
    if (!justificationDisabled && !justification?.length) {
      toast.warn("Justification Required!");
      return;
    }
    const body = { requestId, disposition, justification } as {
      requestId: number;
      disposition: TDispositionValues;
      justification: string;
    };
    sendDisposition(body);
    setRequestId(null);
    setDisposition("");
    setJustification("");
    setShowConfirmModal(false);
    setTimeout(() => {
      refreshRequestNotifications();
    }, 800);
  }, [
    disposition,
    justification,
    justificationDisabled,
    requestId,
    refreshRequestNotifications,
    sendDisposition,
    setDisposition,
    setJustification,
    setRequestId,
    setShowConfirmModal,
  ]);

  const handleCancelDisposition = React.useCallback(() => {
    setRequestId(null);
    setDisposition("");
    setJustification("");
    setShowConfirmModal(false);
  }, [setDisposition, setJustification, setRequestId, setShowConfirmModal]);

  if (isLoadingAccesses || isLoadingRequests) {
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
        aria-description="container to resource controls"
      >
        <Paginator
          className={styles["admin-paginator"]}
          first={first}
          rows={rows}
          totalRecords={totalRows}
          rowsPerPageOptions={[5, 10, 20]}
          onPageChange={onPageChange}
        />
        <MultiSelect
          value={selectedAccessFilters}
          onChange={handleAccessFilterChange}
          options={FILTER_ACCESS_OPTIONS}
          optionLabel="name"
          filter
          display="chip"
          placeholder="Filter Access"
          maxSelectedLabels={1}
          className={styles["admin-filter"]}
          showSelectAll={false}
          dropdownIcon={<FontAwesomeIcon icon={faFilter} />}
          data-tooltip-id="filter-tooltip"
          data-tooltip-delay-show={500}
        />
        {superuserPermissions && (
          <MultiSelect
            value={selectedStageFilters}
            onChange={handleStageFilterChange}
            options={FILTER_STAGES_OPTIONS}
            optionLabel="name"
            filter
            display="chip"
            placeholder="Filter Stages"
            maxSelectedLabels={1}
            className={styles["admin-filter"]}
            showSelectAll={false}
            dropdownIcon={<FontAwesomeIcon icon={faFilter} />}
            data-tooltip-id="filter-tooltip"
            data-tooltip-delay-show={500}
          />
        )}
        <MultiSelect
          value={selectedSubFunctionFilters}
          onChange={handleSubFunctionFilterChange}
          options={FILTER_SUBFUNCTION_OPTIONS}
          optionLabel="name"
          filter
          display="chip"
          placeholder="Filter SubFunctions"
          className={styles["admin-filter"]}
          showSelectAll={false}
          dropdownIcon={<FontAwesomeIcon icon={faFilter} />}
          data-tooltip-id="filter-tooltip"
          data-tooltip-delay-show={500}
        />
        <Tooltip id="filter-tooltip" place={"left-start"}>
          Filter Resources
        </Tooltip>
        {isFetchingRequests && (
          <div
            className={styles["admin-filter-loading"]}
            aria-description="container to display when loading data with filters"
          >
            <MoonLoader size={30} />
          </div>
        )}
      </div>
      {isLoadingRequests ? (
        <div
          className={styles["admin-loading"]}
          aria-description="container to display when loading initial data"
        >
          <MoonLoader />
        </div>
      ) : !isFetchingRequests && !requests?.data.length ? (
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
                    locked={true}
                  >
                    {() => (
                      <div aria-description="container for a resource request">
                        <Form
                          disabled={true}
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
                        <div
                          className={`${styles["button-container"]} ${styles["button-container-evenly-spaced"]}`}
                          aria-description="container for button components"
                        >
                          <button
                            className={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
                            onClick={(event) =>
                              handleDisposition(
                                request.id,
                                DISPOSITION_VALUES.REJECTED
                              )(event)
                            }
                            aria-label="reject resource request"
                          >
                            Reject
                          </button>
                          <button
                            className={`${styles["admin-button"]} ${styles["admin-button-revise"]}`}
                            onClick={(event) =>
                              handleDisposition(
                                request.id,
                                DISPOSITION_VALUES.REVISE
                              )(event)
                            }
                            aria-label="revise resource request"
                          >
                            Revise
                          </button>
                          <span
                            data-tooltip-id={
                              request.originator.user.email ===
                              loaderData.user.email
                                ? `approve-tooltip-${request.id}`
                                : ""
                            }
                            data-tooltip-delay-show={200}
                            aria-description="container for the approve resource request button "
                          >
                            <button
                              className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
                              onClick={(event) =>
                                handleDisposition(
                                  request.id,
                                  DISPOSITION_VALUES.APPROVED
                                )(event)
                              }
                              aria-label="approve resource request"
                              disabled={
                                request.originator.user.email ===
                                loaderData.user.email
                              }
                            >
                              Approve
                            </button>
                          </span>
                          <Tooltip
                            id={`approve-tooltip-${request.id}`}
                            place={"left-start"}
                          >
                            Cannot approve your own requests.
                          </Tooltip>
                        </div>
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
        title={`${/(.*?(VE|T|SE))E?D?|(REJECT)ED/.exec(disposition)?.[1]} Resource Request`}
        open={showConfirmModal}
        acceptLabel={<>{confirmDispositionButtonLabel}</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleConfirmDisposition()}
        onReject={() => handleCancelDisposition()}
        acceptClassName={`${styles["admin-button"]} ${confirmDispositionButtonStyle}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
        className={styles["formcard-modal"]}
      >
        {justificationDisabled ? (
          <></>
        ) : (
          <div style={{ marginTop: "0.5rem" }}>
            <FloatLabel>
              <InputTextarea
                id="Justification"
                value={justification}
                onChange={(event: React.ChangeEvent<HTMLTextAreaElement>) =>
                  setJustification(event.target.value)
                }
                rows={10}
                cols={100}
              />
              <label htmlFor="Justification">Justification</label>
            </FloatLabel>
          </div>
        )}
      </ConfirmModal>
    </>
  );
}
