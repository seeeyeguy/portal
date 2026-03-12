import React from "react";
import { useLoaderData } from "react-router-dom";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import { faFilter, faLock, faLockOpen, faPlus, faWrench } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import { FilterMatchMode } from "primereact/api";
import { AutoComplete, AutoCompleteCompleteEvent } from "primereact/autocomplete";
import { Checkbox } from "primereact/checkbox";
import { Column } from "primereact/column";
import { DataTable, DataTableFilterMeta } from "primereact/datatable";
import FormType from "@rjsf/core";
import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import ProgressBar, { IProgressMarker } from "views/components/ProgressBar/ProgressBar";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";
import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";
import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { IDisposition } from "definitions/portal/request/Disposition.types";
import { IRequest } from "definitions/portal/request/Request.types";
import { ITransition, ITransitionGraph } from "definitions/portal/request/Transition.types";
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
import { useRefreshRequestNotificationsMutation } from "state/query/api/portal/request/RequestNotificationApi";

import {
  resourceCustomValidate,
  ResourceFormData,
  resourceSchema,
  resourceUiSchema,
  resourceWidgets,
  transformResourceToFormData,
} from "views/schemas/administration/ResourceSchema";
import { ERequestStage } from "views/definitions/Request.types";

import { hasSuperuserPermissions } from "utils/PermissionUtility";
import { debounce, resolveApiErrorMessage } from "utils/PromiseUtility";
import { base64ImageToFile } from "views/utils/ImageUtility";
import {
  getThumbnailPath,
  resourceTypeThumbnailPaths,
} from "views/utils/ResourceLinksUtility";

import styles from "views/containers/AdminControls/AdminControls.module.css";

const EDITABLE_STAGES = [1, 4];
const DRAFT = "DRAFT";
const SUBMITTED = "SUBMITTED";
const COLUMN_SETTINGS_STORAGE_KEY = "requestsColumnSettings";

const STAGE_MAPPING_MISC: {
  [key in ERequestStage]: { status: string; color: string };
} = {
  [ERequestStage.DRAFT]: { status: "DRAFT", color: "#5bc0de" },
  [ERequestStage.SUBMITTED]: { status: "PENDING", color: "#5bc0de" },
  [ERequestStage.APPROVED_BUSINESS_PROCESS_EXPERT]: {
    status: "PENDING",
    color: "#5bc0de",
  },
  [ERequestStage.REVISE]: { status: "REVISION", color: "#fcaf29" },
  [ERequestStage.REJECTED_BUSINESS_PROCESS_EXPERT]: {
    status: "REJECTED",
    color: "#ff0000",
  },
  [ERequestStage.APPROVED_SUPERUSER]: { status: "APPROVED", color: "#4fd68e" },
  [ERequestStage.REJECTED_SUPERUSER]: { status: "REJECTED", color: "#ff0000" },
};

const STAGE_MAPPING_MARKER: { [key in ERequestStage]: IProgressMarker & { shortLabel: string, fullLabel: string } } = {
  [ERequestStage.DRAFT]: {
    id: 0,
    shortLabel: "Request Created",
    fullLabel: "Request Created",
    complete: true,
  },
  [ERequestStage.SUBMITTED]: {
    id: 1,
    shortLabel: "Awaiting BPE Approval",
    fullLabel: "Awaiting Business Process Expert Approval",
    complete: true,
  },
  [ERequestStage.APPROVED_BUSINESS_PROCESS_EXPERT]: {
    id: 2,
    shortLabel: "Awaiting SU Approval",
    fullLabel: "Awaiting Superuser Approval",
    complete: true,
  },
  [ERequestStage.REVISE]: {
    id: 0,
    shortLabel: "Revision Requested",
    fullLabel: "Revision Requested",
    complete: true,
  },
  [ERequestStage.REJECTED_BUSINESS_PROCESS_EXPERT]: {
    id: 3,
    shortLabel: "Rejected by BPE",
    fullLabel: "Rejected by Business Process Expert",
    complete: true,
  },
  [ERequestStage.APPROVED_SUPERUSER]: {
    id: 3,
    shortLabel: "Request Approved",
    fullLabel: "Request Approved",
    complete: true,
  },
  [ERequestStage.REJECTED_SUPERUSER]: {
    id: 3,
    shortLabel: "Rejected by SU",
    fullLabel: "Rejected by Superuser",
    complete: true,
  },
};

const INITIAL_MARKERS: IProgressMarker[] = [
  { id: 0, complete: false, completeLabel: "", incompleteLabel: "" },
  { id: 1, complete: false, completeLabel: "", incompleteLabel: "" },
  { id: 2, complete: false, completeLabel: "", incompleteLabel: "" },
  { id: 3, complete: false, completeLabel: "", incompleteLabel: "" },
];

interface ColumnConfig {
  key: string;
  label: string;
  visible: boolean;
  default: boolean;
}

const DEFAULT_COLUMNS: ColumnConfig[] = [
  { key: "name", label: "Name", visible: true, default: true },
  { key: "url", label: "URL", visible: true, default: true },
  { key: "subfunction", label: "SubFunction", visible: true, default: true },
  { key: "function", label: "Function", visible: true, default: true },
  { key: "progress", label: "Progress", visible: true, default: true },
  { key: "requestor", label: "Requestor", visible: true, default: true },
  { key: "pointOfContact", label: "Point of Contact", visible: false, default: false },
  { key: "lastUpdated", label: "Last Updated", visible: true, default: true },
  { key: "thumbnail", label: "Thumbnail", visible: false, default: false }, 
  { key: "tags", label: "Tags", visible: false, default: false },
  { key: "lock", label: "Is Locked", visible: false, default: false },
  { key: "revision", label: "Is Revision", visible: false, default: false },
];

const getLatestTransitions = (transitions: ITransitionGraph): ITransition[] => {
  const nodes: ITransition[] = [];
  let currentTransitionId: number | null = transitions.latest;

  while (currentTransitionId) {
    const currentNode: ITransition = transitions.nodes[currentTransitionId];

    if (currentNode.stage.id === ERequestStage.DRAFT) {
      if (currentNode.previousTransition) {
        nodes.push(transitions.nodes[currentNode.previousTransition]);
      } else {
        nodes.push(currentNode);
      }
      break;
    }

    nodes.push(currentNode);
    currentTransitionId = currentNode.previousTransition;
  }

  return nodes;
};

const getProgressTooltipContent = (
  request: IRequest,
  latestTransition: ERequestStage,
  styles: { readonly [key: string]: string }
): JSX.Element => {
  const revisionPreviousTransition = request.transitions.nodes[request.transitions.latest];

  const getDispositionDetails = (dispositions: IDisposition[]) => {
    if (!dispositions || dispositions.length === 0) return null;
    const latestDisposition = dispositions[dispositions.length - 1];
    const { disposition, created, approver, justification } = latestDisposition;
    const { firstName, lastName } = approver.user;

    return (
      <>
        <p>
          {`${disposition} - ${new Date(created).toLocaleString("en-US", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
          })} - ${firstName} ${lastName}`}
        </p>
        {justification && <p>Justification - {justification ?? "N/A"}</p>}
      </>
    );
  };

  const previousTransition = revisionPreviousTransition.previousTransition;
  const previousTransitionDispositions = previousTransition
    ? (request.transitions.nodes[previousTransition].dispositions as IDisposition[])
    : [];

  const isDraftStage = revisionPreviousTransition.stage.level === 1;
  const revisionDispositionPrevious = isDraftStage
    ? revisionPreviousTransition.previousTransition
    : null;
  const revisionDispositionRevisionTransition = revisionDispositionPrevious
    ? request.transitions.nodes[revisionDispositionPrevious].previousTransition
    : null;
  const revisionDisposition = revisionDispositionRevisionTransition
    ? (request.transitions.nodes[revisionDispositionRevisionTransition]
        .dispositions as IDisposition[])
    : [];

  const dispositionDetails = previousTransitionDispositions.length
    ? getDispositionDetails(previousTransitionDispositions)
    : getDispositionDetails(revisionDisposition);

  const fullProgressName = STAGE_MAPPING_MARKER[latestTransition]?.fullLabel || "";

  return (
    <>
      <div className={styles["tooltip-title"]} aria-label="Progress status title">
        {fullProgressName}
      </div>
      <b>{`Submitted by - ${request.originator.user.firstName} ${request.originator.user.lastName}`}</b>
      <p>Current Transition - {request.transitions.nodes[request.transitions.latest].stage.name}</p>
      {dispositionDetails}
    </>
  );
};

export default function RequestsControls() {
  const loaderData = useLoaderData() as { user: IAuthUser };

  const superuserPermissions = React.useMemo(
    () => hasSuperuserPermissions(loaderData.user),
    [loaderData]
  );

  const [showDrafts, setShowDrafts] = React.useState(false);
  const [showColumnFilter, setShowColumnFilter] = React.useState(false);

  const [filters, setFilters] = React.useState<DataTableFilterMeta>({
    "resource.name": { value: null, matchMode: FilterMatchMode.CONTAINS },
    "resource.url": { value: null, matchMode: FilterMatchMode.CONTAINS },
    "subfunctionNames": { value: null, matchMode: FilterMatchMode.CONTAINS },
    "functionNames": { value: null, matchMode: FilterMatchMode.CONTAINS },
    "primaryPoc": { value: null, matchMode: FilterMatchMode.CONTAINS },
    "tagNames": { value: null, matchMode: FilterMatchMode.CONTAINS },
  });
  
  const [columnSettings, setColumnSettings] = React.useState<ColumnConfig[]>(() => {
    try {
      const saved = localStorage.getItem(COLUMN_SETTINGS_STORAGE_KEY);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (error) {
      console.error("Error loading column settings from localStorage:", error);
    }
    return DEFAULT_COLUMNS;
  });

  React.useEffect(() => {
    try {
      localStorage.setItem(COLUMN_SETTINGS_STORAGE_KEY, JSON.stringify(columnSettings));
    } catch (error) {
      console.error("Error saving column settings to localStorage:", error);
    }
  }, [columnSettings]);

  const toggleColumn = (key: string) => {
    setColumnSettings(prev =>
      prev.map(col =>
        col.key === key ? { ...col, visible: !col.visible } : col
      )
    );
  };

  const [filteredSubFunctions, setFilteredSubFunctions] = React.useState<{ name: string; value: number }[]>([]);
  const [filteredFunctions, setFilteredFunctions] = React.useState<{ name: string; value: number }[]>([]);

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

  const { data: subfunctions, isLoading: isSubfunctionsLoading } =
    useGetSubFunctionsQuery(null);

  const {
    data: requests,
    isLoading,
    isFetching,
  } = useGetRequestsQuery({
    originator: null,
    status: "PENDING",
    stages: showDrafts ? [1, 2, 4] : [2, 4],
    subfunctions: null,
    page: null,
    limit: null,
    deleted: null,
  });

  // Filter requests client-side based on user permissions
  const filteredRequests = React.useMemo(() => {
    const allRequests = requests?.data ?? [];
    
    // If superuser, show all requests
    if (superuserPermissions) {
      return allRequests;
    }
    
    // Otherwise, filter to only show requests for subfunctions the user has access to
    return allRequests.filter(request => 
      request.resource.subfunctions.some(sf => 
        usersPermittedSubFunctions.includes(sf.id)
      )
    );
  }, [requests, superuserPermissions, usersPermittedSubFunctions]);

  const requestsWithComputedFields = React.useMemo(() => {
    return filteredRequests.map((req) => ({
      ...req,
      functionNames: Array.from(
        new Set(req.resource.subfunctions.map((sf) => sf.function.name))
      ).join(", "),
      subfunctionNames: req.resource.subfunctions.map((sf) => sf.name).join(", "),
      primaryPoc: req.resource.primaryPointOfContact || "",
      tagNames: req.resource.tags?.map(tag => tag.label).join(", ") || "",
    }));
  }, [filteredRequests]);

  const [updateResource] = useUpdateRequestMutation();
  const [addResource] = useAddRequestMutation();
  const [removeRequest] = useRemoveRequestMutation();
  const [refreshRequestNotifications] = useRefreshRequestNotificationsMutation();

  const { data: tags } = useGetTagsQuery(null);
  const { data: employeeLevels, isLoading: isEmployeeLevelsLoading } =
    useGetEmployeeLevelsAdminQuery(null);
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
              name: record.name,
              value: record.id,
            },
          ];
        },
        [] as { name: string; value: number }[]
      ),
    [subfunctions, superuserPermissions, usersPermittedSubFunctions]
  );

  const filterFunctionOptions = React.useMemo(() => {
    const functionMap = new Map<number, string>();
    ((subfunctions?.data ?? []) as ISubFunction[]).forEach((record) => {
      if (
        superuserPermissions ||
        usersPermittedSubFunctions.includes(record.id)
      ) {
        functionMap.set(record.function.id, record.function.name);
      }
    });
    return Array.from(functionMap.entries()).map(([id, name]) => ({
      name,
      value: id,
    }));
  }, [subfunctions, superuserPermissions, usersPermittedSubFunctions]);

  const searchSubFunctions = (event: AutoCompleteCompleteEvent) => {
    const query = event.query.toLowerCase();
    const filtered = filterSubfunctionOptions.filter((option) =>
      option.name.toLowerCase().includes(query)
    );
    setFilteredSubFunctions(filtered);
  };

  const searchFunctions = (event: AutoCompleteCompleteEvent) => {
    const query = event.query.toLowerCase();
    const filtered = filterFunctionOptions.filter((option) =>
      option.name.toLowerCase().includes(query)
    );
    setFilteredFunctions(filtered);
  };

  const fetchUserOptions = React.useCallback(
    async (searchTerm: string): Promise<string[]> => {
      if (!searchTerm?.length) return [];

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
      return (data?.data ?? []).map((employee) => employee.email);
    },
    []
  );

  const debouncedFetchPoc = React.useMemo(
    () => debounce(fetchUserOptions, 300),
    [fetchUserOptions]
  );

  const [showNewModal, setShowNewModal] = React.useState(false);
  const [showEditModal, setShowEditModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState<number | null>(null);
  const [selectedRequest, setSelectedRequest] = React.useState<IRequest | null>(null);

  const newFormRef = React.useRef<FormType>(null);
  const editFormRef = React.useRef<FormType>(null);
  const [newFormKey, setNewFormKey] = React.useState(Date.now());
  const [editFormKey, setEditFormKey] = React.useState(Date.now());

  const isRequestEditable = React.useCallback((request: IRequest | null): boolean => {
    if (!request) return false;
    const latestTransition = request.transitions?.nodes[request.transitions.latest];
    const stageLevel = latestTransition?.stage?.level;
    return EDITABLE_STAGES.includes(stageLevel);
  }, []);

  const updatedUiSchema = React.useMemo(() => {
    const isEditable = selectedRequest ? isRequestEditable(selectedRequest) : true;
    
    if (tags) {
      return {
        ...resourceUiSchema,
        tags: {
          ...resourceUiSchema.tags,
          "ui:options": { 
            tags: tags.data,
          },
          "ui:readonly": !isEditable,
        },
        primaryPoc: {
          ...resourceUiSchema.primaryPoc,
          "ui:options": {
            completeMethod: (searchTerm: string) => debouncedFetchPoc(searchTerm),
          },
        },
        "ui:submitButtonOptions": {
          norender: true,
        },
      };
    }
    return resourceUiSchema;
  }, [tags, debouncedFetchPoc, selectedRequest, isRequestEditable]);

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

  const handleFormSubmit = React.useCallback(
    async (stage: "DRAFT" | "SUBMITTED", isEdit: boolean) => {
      const formRef = isEdit ? editFormRef.current : newFormRef.current;

      if (formRef && formRef.validateForm()) {
        const formSubmission: ResourceFormData = {
          ...formRef.state.formData,
        };

        const body: TApiPostRequestRequest | TApiPutRequestRequest = {
          ...formSubmission,
          pointOfContacts: [
            formSubmission.primaryPoc,
          ],
          thumbnail: base64ImageToFile(formSubmission.thumbnail as string),
          stage,
          ...(isEdit ? {} : { uid: null, previousRevision: null }),
        };

        const response = isEdit
          ? await updateResource({ body: body as TApiPutRequestRequest, id: selectedRequest!.id })
          : await addResource(body as TApiPostRequestRequest);

        if (response.error) {
          const message =
            "data" in response.error
              ? resolveApiErrorMessage(response.error.data as string | object)
              : DEFAULT_API_ERROR_MESSAGE;

          console.error(message);
          toast.error(`Error Saving Request: ${message}`);
        } else {
          toast.success(isEdit ? "Request Updated" : "Request Created");
          refreshRequestNotifications();
          if (isEdit) {
            setShowEditModal(false);
            setSelectedRequest(null);
          } else {
            setShowNewModal(false);
            setNewFormKey(Date.now());
          }
        }
      }
    },
    [addResource, updateResource, refreshRequestNotifications, selectedRequest]
  );

  const handleCreate = React.useCallback(
    (stage: "DRAFT" | "SUBMITTED") => handleFormSubmit(stage, false),
    [handleFormSubmit]
  );

  const handleEdit = React.useCallback(
    (stage: "DRAFT" | "SUBMITTED") => handleFormSubmit(stage, true),
    [handleFormSubmit]
  );

  const handleRowClick = (request: IRequest) => {
    setSelectedRequest(request);
    setEditFormKey(Date.now());
    setShowEditModal(true);
  };

  const createProgressMarkers = React.useCallback(
    (transitions: ITransitionGraph): [IProgressMarker[], ERequestStage] => {
      const newLatestTransitions = getLatestTransitions(transitions);
      const newProgressMarkers = INITIAL_MARKERS.map((a) => ({ ...a }));

      newLatestTransitions.forEach((transition) => {
        const tempProgressMarker =
          STAGE_MAPPING_MARKER[transition.stage.id as ERequestStage];
        if (lodash.isNumber(tempProgressMarker.id)) {
          newProgressMarkers[tempProgressMarker.id] = { ...tempProgressMarker };

          for (let i = 0; i <= tempProgressMarker.id; i++) {
            newProgressMarkers[i].complete = true;
          }
        }
      });
      return [
        newProgressMarkers,
        newLatestTransitions[0].stage.id ?? ERequestStage.DRAFT,
      ];
    },
    []
  );

  // Column body templates
  const nameBodyTemplate = (rowData: IRequest) => (
    <div aria-label="Resource name and deletion status">
      <div className={styles["resource-name"]} aria-label={`Resource name: ${rowData.resource.name}`}>
        {rowData.resource.name}
      </div>
      {rowData.resource.deleted && (
        <span
          className={
            rowData.resource.active === false
              ? styles["resource-marked-for-deletion"]
              : styles["resource-deleted"]
          }
          aria-label={rowData.resource.active === false ? "Marked for deletion" : "Deleted"}
        >
          {rowData.resource.active === false
            ? "(Marked for Deletion)"
            : "(Deleted)"}
        </span>
      )}
    </div>
  );

  const urlBodyTemplate = (rowData: IRequest) => (
    <div 
      className={styles["resource-url"]} 
      title={rowData.resource.url} 
      aria-label={`Resource URL: ${rowData.resource.url}`}
    >
      {rowData.resource.url}
    </div>
  );

  const subfunctionBodyTemplate = (rowData: IRequest) => {
    const subfunctions = rowData.resource.subfunctions
      .map((sf) => sf.name)
      .join(", ");
    return <span aria-label={`Subfunctions: ${subfunctions}`}>{subfunctions}</span>;
  };

  const functionBodyTemplate = (rowData: IRequest) => {
    const functions = Array.from(
      new Set(rowData.resource.subfunctions.map((sf) => sf.function.name))
    ).join(", ");
    return <span aria-label={`Functions: ${functions}`}>{functions}</span>;
  };

  const progressBodyTemplate = (rowData: IRequest) => {
    const [progressMarkers, latestTransition] = createProgressMarkers(
      rowData.transitions
    );

    const displayMarkers = progressMarkers.map((marker) => {
      const stage = Object.keys(STAGE_MAPPING_MARKER).find(
        key => STAGE_MAPPING_MARKER[key as unknown as ERequestStage].id === marker.id
      ) as ERequestStage | undefined;
      return stage
        ? { ...marker, completeLabel: STAGE_MAPPING_MARKER[stage].shortLabel }
        : marker;
    });

    return (
      <div 
        className={styles["progress-bar-wrapper"]}
        data-tooltip-id={`progress-tooltip-${rowData.id}`}
        aria-label={`Request progress: ${STAGE_MAPPING_MARKER[latestTransition]?.shortLabel || 'Unknown'}`}
      >
        <ProgressBar
          progressColor={STAGE_MAPPING_MISC[latestTransition].color}
          totalCompletionLabel=""
          centeredLabel={true}
          discreteUnit=""
          currentMarker={
            latestTransition ? STAGE_MAPPING_MARKER[latestTransition].id : null
          }
          progressMarkers={displayMarkers}
        />
      </div>
    );
  };

  const lockBodyTemplate = (rowData: IRequest) => {
    const isLocked = !isRequestEditable(rowData);

    return (
      <div 
        className={styles["icon-cell"]} 
        aria-label={isLocked ? "Request is locked and cannot be edited" : "Request is unlocked and can be edited"}
      >
        <FontAwesomeIcon
          icon={isLocked ? faLock : faLockOpen}
          data-tooltip-id={`locked-tooltip-${rowData.id}`}
          className={styles["icon-clickable"]}
        />
      </div>
    );
  };

  const revisionBodyTemplate = (rowData: IRequest) => {
    const isRevision = !!rowData.resource.previousRevision;

    return (
      <div 
        className={styles["icon-cell"]} 
        aria-label={isRevision ? "This is a revision of an existing resource" : "Not a revision"}
      >
        {isRevision && (
          <FontAwesomeIcon
            icon={faWrench}
            data-tooltip-id={`revision-tooltip-${rowData.id}`}
            className={styles["icon-clickable"]}
          />
        )}
      </div>
    );
  };

  const originatorBodyTemplate = (rowData: IRequest) => (
    <span aria-label={`Requestor: ${rowData.originator?.user?.firstName} ${rowData.originator?.user?.lastName}`}>
      {rowData.originator?.user?.firstName} {rowData.originator?.user?.lastName}
    </span>
  );

  const pointOfContactBodyTemplate = (rowData: { primaryPoc: string }) => (
    <div 
      className={styles["resource-poc"]} 
      aria-label={`Point of contact: ${rowData.primaryPoc}`}
    >
      {rowData.primaryPoc}
    </div>
  );

  const tagsBodyTemplate = (rowData: { tagNames: string }) => (
    <div 
      className={styles["resource-tags"]} 
      aria-label={`Resource tags: ${rowData.tagNames || 'None'}`}
    >
      {rowData.tagNames}
    </div>
  );

  const thumbnailBodyTemplate = (rowData: IRequest) => {
    const thumbnailPath = getThumbnailPath(rowData.resource);
    return (
      <img 
        src={thumbnailPath} 
        alt={`${rowData.resource.name} thumbnail`}
        className={styles["resource-thumbnail"]}
        aria-label={`Thumbnail for ${rowData.resource.name}`}
      />
    );
  };

  const getColumnByKey = (key: string) => {
    const config = columnSettings.find(col => col.key === key);
    if (!config?.visible) return null;

    switch (key) {
      case "name":
        return (
          <Column
            key={key}
            field="resource.name"
            header="Name"
            body={nameBodyTemplate}
            filter
            filterPlaceholder="Filter by Name"
            filterMatchMode="contains"
            sortable
            style={{minWidth: "250px"}}
            showFilterMenu={false}
          />
        );
      case "url":
        return (
          <Column
            key={key}
            field="resource.url"
            header="URL"
            body={urlBodyTemplate}
            filter
            filterPlaceholder="Filter by URL"
            filterMatchMode="contains"
            sortable
            style={{minWidth: "250px"}}
            showFilterMenu={false}
          />
        );
      case "subfunction":
        return (
          <Column
            key={key}
            field="subfunctionNames"
            header="SubFunction"
            body={subfunctionBodyTemplate}
            sortable
            style={{minWidth: "270px"}}
            filter
            showFilterMenu={false}
            filterElement={(options) => (
              <AutoComplete
                value={options.value || ""}
                suggestions={filteredSubFunctions}
                completeMethod={searchSubFunctions}
                field="name"
                dropdown
                onChange={(e) => {
                  const value = e.value;
                  if (typeof value === 'object' && value?.name) {
                    if (options.filterApplyCallback) {
                      options.filterApplyCallback(value.name);
                    } else {
                      options.filterCallback(value.name);
                    }
                  } else if (typeof value === 'string') {
                    if (options.filterApplyCallback) {
                      options.filterApplyCallback(value);
                    } else {
                      options.filterCallback(value);
                    }
                  } else {
                    if (options.filterApplyCallback) {
                      options.filterApplyCallback("");
                    } else {
                      options.filterCallback("");
                    }
                  }
                }}
                placeholder="Filter by SubFunction"
                forceSelection={false}
                className={styles["autocomplete-filter"]}
                inputClassName={styles["autocomplete-input"]}
                panelClassName={styles["autocomplete-panel"]}
              />
            )}
          />
        );
      case "function":
        return (
          <Column
            key={key}
            field="functionNames"
            header="Function"
            body={functionBodyTemplate}
            sortable
            style={{minWidth: "240px"}}
            filter
            showFilterMenu={false}
            filterElement={(options) => (
              <AutoComplete
                value={options.value || ""}
                suggestions={filteredFunctions}
                completeMethod={searchFunctions}
                field="name"
                dropdown
                onChange={(e) => {
                  const value = e.value;
                  if (typeof value === 'object' && value?.name) {
                    if (options.filterApplyCallback) {
                      options.filterApplyCallback(value.name);
                    } else {
                      options.filterCallback(value.name);
                    }
                  } else if (typeof value === 'string') {
                    if (options.filterApplyCallback) {
                      options.filterApplyCallback(value);
                    } else {
                      options.filterCallback(value);
                    }
                  } else {
                    if (options.filterApplyCallback) {
                      options.filterApplyCallback("");
                    } else {
                      options.filterCallback("");
                    }
                  }
                }}
                placeholder="Filter by Function"
                forceSelection={false}
                className={styles["autocomplete-filter"]}
                inputClassName={styles["autocomplete-input"]}
                panelClassName={styles["autocomplete-panel"]}
              />
            )}
          />
        );
      case "progress":
        return (
          <Column
            key={key}
            body={progressBodyTemplate}
            header="Progress"
            style={{minWidth: "260px"}}
          />
        );
      case "requestor":
        return (
          <Column
            key={key}
            body={originatorBodyTemplate}
            header="Requestor"
            sortable
            sortField="originator.user.lastName"
            style={{minWidth: "110px"}}
          />
        );
      case "lastUpdated":
        return (
          <Column
            key={key}
            field="modified"
            header="Last Updated"
            sortable
            body={(rowData) => {
              const date = new Date(rowData.modified).toLocaleDateString();
              return <span aria-label={`Last updated: ${date}`}>{date}</span>;
            }}
            style={{minWidth: "130px"}}
          />
        );
      case "lock":
        return (
          <Column
            key={key}
            field="isLocked"
            body={lockBodyTemplate}
            header=""
            style={{minWidth: "50px", textAlign: "center" }}
            filter={false}
            sortable={false}
          />
        );
      case "revision":
        return (
          <Column
            key={key}
            field="isRevision"
            body={revisionBodyTemplate}
            header=""
            style={{minWidth: "50px", textAlign: "center" }}
            filter={false}
            sortable={false}
          />
        );
      case "pointOfContact":
        return (
          <Column
            key={key}
            field="primaryPoc"
            body={pointOfContactBodyTemplate}
            header="Point of Contact"
            filter
            filterPlaceholder="Filter by POC"
            filterMatchMode="contains"
            sortable
            style={{minWidth: "200px"}}
            showFilterMenu={false}
          />
        );
      case "tags":
        return (
          <Column
            key={key}
            field="tagNames"
            header="Tags"
            body={tagsBodyTemplate}
            filter
            filterPlaceholder="Filter by Tags"
            filterMatchMode="contains"
            sortable
            style={{minWidth: "220px"}}
            showFilterMenu={false}
          />
        );
      case "thumbnail":
        return (
          <Column
            key={key}
            body={thumbnailBodyTemplate}
            header="Thumbnail"
            style={{minWidth: "100px"}}
          />
        );
      default:
        return null;
    }
  };

  if (isLoading) {
    return (
      <div className={styles["admin-loading"]} aria-label="Loading requests data">
        <MoonLoader />
      </div>
    );
  }

  return (
    <div className={styles["requests-page"]} aria-label="Requests management page">
      <div className={styles["admin-controls"]} aria-label="Request controls and filters section">
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          disabled={isEmployeeLevelsLoading || isSubfunctionsLoading}
          onClick={() => setShowNewModal(true)}
          aria-label="Add new resource request"
        >
          <FontAwesomeIcon icon={faPlus} />
          Add Resource
        </button>

        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          onClick={() => setShowColumnFilter(!showColumnFilter)}
          data-tooltip-id="filter-tooltip"
          data-tooltip-delay-show={500}
          aria-label="Toggle column visibility filter"
        >
          <FontAwesomeIcon icon={faFilter} />
          Columns
        </button>
        <Tooltip
          id="filter-tooltip"
          place="top"
          className={styles["filter-tooltip-style"]}
        >
          Show/Hide Columns
        </Tooltip>

        <div className={styles["admin-deleted-checkbox"]} aria-label="Show drafts checkbox control">
          <Checkbox
            inputId="showDrafts"
            checked={showDrafts}
            onChange={(e) => setShowDrafts(!!e.checked)}
          />
          <label htmlFor="showDrafts">Show Drafts</label>
        </div>

        {isFetching && (
          <div className={styles["admin-filter-loading"]} aria-label="Loading filtered results">
            <MoonLoader size={30} />
          </div>
        )}
      </div>

      {showColumnFilter && (
        <div className={styles["column-filter-panel"]} aria-label="Column filter options panel">
          <h4 className={styles["column-filter-title"]}>Show/Hide Columns</h4>
          <div className={styles["column-filter-grid"]} aria-label="Column visibility toggles grid">
            {columnSettings.map((col) => (
              <div key={col.key} className={styles["column-filter-item"]} aria-label={`Toggle ${col.label} column visibility`}>
                <Checkbox
                  inputId={`col-${col.key}`}
                  checked={col.visible}
                  onChange={() => toggleColumn(col.key)}
                />
                <label htmlFor={`col-${col.key}`} className={styles["column-filter-label"]}>
                  {col.label || col.key}
                </label>
              </div>
            ))}
          </div>
        </div>
      )}

      <div 
        className={showColumnFilter ? styles["table-wrapper-with-filter"] : styles["table-wrapper"]}
        aria-label="Requests data table container"
      >
        <DataTable
          value={requestsWithComputedFields}
          scrollable
          scrollHeight="flex"
          tableStyle={{ minWidth: "500px"}}
          filterDisplay="row"
          emptyMessage="No Pending Requests Found"
          onRowClick={(e) => handleRowClick(e.data as IRequest)}
          rowHover
          className={styles["data-table"]}
          sortMode="multiple"
          loading={isFetching}
          filters={filters}
          onFilter={(e) => setFilters(e.filters)}
        >
          {columnSettings.map((col) => getColumnByKey(col.key))}
        </DataTable>
      </div>

      {/* Tooltip Portal - Renders all tooltips outside the table */}
      <div style={{ position: 'fixed', top: 0, left: 0, pointerEvents: 'none'}} aria-hidden="true">
        {requestsWithComputedFields.map((request) => {
          const [, latestTransition] = createProgressMarkers(request.transitions);
          const isLocked = !isRequestEditable(request);
          const isRevision = !!request.resource.previousRevision;
          
          return (
            <React.Fragment key={request.id}>
              <Tooltip 
                id={`progress-tooltip-${request.id}`} 
                place="left"
                className={styles["tooltip-style"]}
                offset={10}
              >
                {getProgressTooltipContent(request, latestTransition, styles)}
              </Tooltip>
              
              <Tooltip 
                id={`locked-tooltip-${request.id}`} 
                place="left"
                className={styles["tooltip-style"]}
                offset={10}
              >
                {isLocked
                  ? "This request has been submitted and cannot be edited"
                  : "This request can be edited"}
              </Tooltip>
              
              {isRevision && (
                <Tooltip 
                  id={`revision-tooltip-${request.id}`} 
                  place="left"
                  className={styles["tooltip-style"]}
                  offset={10}
                >
                  This is a revision of an existing resource
                </Tooltip>
              )}
            </React.Fragment>
          );
        })}
      </div>

      <ConfirmModal
        title="Add Resource"
        open={showNewModal}
        acceptLabel={<>Request Approval</>}
        alternativeLabel={<>Save Draft</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleCreate(SUBMITTED)}
        onAlternative={() => handleCreate(DRAFT)}
        onReject={() => {
          setShowNewModal(false);
          setNewFormKey(Date.now());
        }}
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

      <ConfirmModal
        title={isRequestEditable(selectedRequest) ? "Edit Request" : "View Request"}
        open={showEditModal}
        acceptLabel={isRequestEditable(selectedRequest) ? <>Submit Revision</> : undefined}
        alternativeLabel={
          isRequestEditable(selectedRequest)
            ? selectedRequest?.resource.deleted
              ? <>Submit Deletion</>
              : <>Save Draft</>
            : undefined
        }
        rejectLabel={isRequestEditable(selectedRequest) ? <>Cancel</> : undefined}
        onAccept={
          isRequestEditable(selectedRequest)
            ? () => handleEdit(SUBMITTED)
            : undefined
        }
        onAlternative={
          isRequestEditable(selectedRequest)
            ? selectedRequest?.resource.deleted
              ? () => setShowDeleteModal(selectedRequest.id)
              : () => handleEdit(DRAFT)
            : undefined
        }
        onReject={
          isRequestEditable(selectedRequest)
            ? () => {
                setShowEditModal(false);
                setSelectedRequest(null);
              }
            : undefined
        }
        onHide={() => {
          setShowEditModal(false);
          setSelectedRequest(null);
        }}
        acceptClassName={
          isRequestEditable(selectedRequest)
            ? `${styles["admin-button"]} ${styles["admin-button-submit"]}`
            : undefined
        }
        alternativeClassName={
          isRequestEditable(selectedRequest)
            ? `${styles["admin-button"]} ${
                selectedRequest?.resource.deleted
                  ? styles["admin-button-delete"]
                  : styles["admin-button-save"]
              }`
            : undefined
        }
        rejectClassName={
          isRequestEditable(selectedRequest)
            ? `${styles["admin-button"]} ${styles["admin-button-cancel"]}`
            : undefined
        }
        className={styles["new-modal-form"]}
      >
        {selectedRequest && (
          <Form
            key={editFormKey}
            ref={editFormRef}
            formData={transformResourceToFormData(selectedRequest.resource)}
            validator={validator}
            customValidate={resourceCustomValidate}
            schema={updatedSchema}
            uiSchema={updatedUiSchema}
            showErrorList={false}
            noHtml5Validate={true}
            widgets={resourceWidgets}
            disabled={!isRequestEditable(selectedRequest)}
          />
        )}
      </ConfirmModal>

      <ConfirmModal
        title="Submit Resource Deletion"
        open={!!showDeleteModal}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={async () => {
          const req = requests?.data.find((r) => r.id === showDeleteModal);

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
          setShowEditModal(false);
        }}
        onReject={() => setShowDeleteModal(null)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
    </div>
  );
}