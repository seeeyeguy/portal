import React from "react";
import { Tooltip } from "react-tooltip";
import { faQuestionCircle } from "@fortawesome/free-regular-svg-icons";
import {
  faAngleDown,
  faAngleRight,
  faLock,
  faLockOpen,
  faWrench,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";

import ProgressBar, {
  IProgressMarker,
} from "views/components/ProgressBar/ProgressBar";

import { IRequest } from "definitions/portal/request/Request.types";
import {
  ITransition,
  ITransitionGraph,
} from "definitions/portal/request/Transition.types";
import { ERequestStage } from "views/definitions/Request.types";

import styles from "views/components/ResourceRequestAccordion/ResourceRequestAccordion.module.css";

// Request Transition mapping to status label and Progressbar color.
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

// Request Transition mapping to Progressbar markers.
const STAGE_MAPPING_MARKER: { [key in ERequestStage]: IProgressMarker } = {
  [ERequestStage.DRAFT]: {
    id: 0,
    completeLabel: "Request Created",
    complete: true,
  },
  [ERequestStage.SUBMITTED]: {
    id: 1,
    completeLabel: "Awaiting Business Process Expert Approval",
    complete: true,
  },
  [ERequestStage.APPROVED_BUSINESS_PROCESS_EXPERT]: {
    id: 2,
    completeLabel: "Awaiting Superuser Approval",
    complete: true,
  },
  [ERequestStage.REVISE]: {
    id: 0,
    completeLabel: "Revision Requested",
    complete: true,
  },
  [ERequestStage.REJECTED_BUSINESS_PROCESS_EXPERT]: {
    id: 3,
    completeLabel: "Rejected by Business Process Expert",
    complete: true,
  },
  [ERequestStage.APPROVED_SUPERUSER]: {
    id: 3,
    completeLabel: "Request Approved",
    complete: true,
  },
  [ERequestStage.REJECTED_SUPERUSER]: {
    id: 3,
    completeLabel: "Rejected by Superuser",
    complete: true,
  },
};

// Markers that represent the steps of a Resource Request.
const INITIAL_MARKERS: IProgressMarker[] = [
  { id: 0, complete: false, completeLabel: "", incompleteLabel: "" },
  { id: 1, complete: false, completeLabel: "", incompleteLabel: "" },
  { id: 2, complete: false, completeLabel: "", incompleteLabel: "" },
  { id: 3, complete: false, completeLabel: "", incompleteLabel: "" },
];

/**
 * Extracts the latest transitions of a Request, up to and including the latest
 * Draft or Revise transition.
 * @param {ITransitionGraph} transitions The transitions of a request.
 * @returns {ITransition[]} The latest transitions of a request.
 */
const getLatestTransitions = (transitions: ITransitionGraph): ITransition[] => {
  const nodes: ITransition[] = [];
  let currentTransitionId: number | null = transitions.latest;

  while (currentTransitionId) {
    const currentNode: ITransition = transitions.nodes[currentTransitionId];

    // If a transition stage is DRAFT then we will push one more transition before breaking.
    if (currentNode.stage.id === ERequestStage.DRAFT) {
      // Check for a REVISION stage and push that instead of the DRAFT stage.
      if (currentNode.previousTransition) {
        nodes.push(transitions.nodes[currentNode.previousTransition]);
      } else {
        nodes.push(currentNode);
      }

      // Stop collecting transitions once we push a Draft or Revise stage.
      break;
    }

    nodes.push(currentNode);
    currentTransitionId = currentNode.previousTransition;
  }

  return nodes;
};

/** Properties for the ResourceRequestAccordion component. */
export interface ResourceRequestAccordionProps {
  /** The `Request` to display. */
  request: IRequest;

  /** The `Resource` thumbnail path. */
  thumbnailPath: string;

  /** How to display the locked icon. */
  locked?: boolean | null;

  /** Request tooltip content. */
  tooltipContent?: JSX.Element | null;

  /** Class selector for the component content. */
  className?: string;

  /** Content to go inside of accordion content details. */
  children: () => React.ReactNode;
}

export default function ResourceRequestAccordion({
  request,
  thumbnailPath,
  locked = null,
  tooltipContent = null,
  className,
  children,
}: ResourceRequestAccordionProps) {
  const [open, setOpen] = React.useState<boolean>(false);
  const [progressMarkers, setProgressMarkers] = React.useState<
    IProgressMarker[]
  >([...INITIAL_MARKERS]);
  const [latestTransition, setLatestTransition] = React.useState<ERequestStage>(
    ERequestStage.DRAFT
  );

  const toggleAccordion = React.useCallback(() => {
    setOpen((state) => !state);
  }, [setOpen]);

  /**
   * Extracts the latest transitions of a Request, up to and including the latest
   * Draft or Revise transition.
   * @param {ITransition[]} transitions An array of transitions.
   * @returns {IProgressMarker[], ERequestStage} An array of progress markers and
   * the stage of the latest transition.
   */
  const createProgressMarkers = React.useCallback(
    (transitions: ITransitionGraph): [IProgressMarker[], ERequestStage] => {
      const newLatestTransitions = getLatestTransitions(transitions);
      const newProgressMarkers = INITIAL_MARKERS.map((a) => ({ ...a }));

      newLatestTransitions.forEach((transition) => {
        const tempProgressMarker =
          STAGE_MAPPING_MARKER[transition.stage.id as ERequestStage];
        if (lodash.isNumber(tempProgressMarker.id)) {
          newProgressMarkers[tempProgressMarker.id] = { ...tempProgressMarker };

          // Verify all previous markers are marked as complete,
          // this allows rejected transitions to be marked as 100% complete.
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

  // When the transitions for a request change, update the progress markers and Request status.
  React.useEffect(() => {
    const [newProgressMarkers, newLatestTransition] = createProgressMarkers(
      request.transitions
    );

    setProgressMarkers(newProgressMarkers);
    setLatestTransition(newLatestTransition);
  }, [request.transitions, createProgressMarkers]);

  return (
    <>
      <details
        className={`${className || ""} ${styles["request-accordion"]}`}
        aria-description={`container for ${request.resource.name} request`}
      >
        <summary
          onClick={toggleAccordion}
          role="button"
          className={styles["request-accordion-summary"]}
          aria-description={`${request.resource.name} accordion summary`}
          data-testid={open ? "accordion-active" : "accordion-inactive"}
        >
          <img
            className={`${styles["thumbnail-link-img"]}`}
            src={thumbnailPath}
            alt={`${request.resource.name} resource thumbnail`}
            width={64}
            height={64}
          />
          <div
            className={styles["request-accordion-details"]}
            aria-description={`${request.resource.name} accordion details`}
            data-testid={open ? "accordion-active" : "accordion-inactive"}
          >
            <div
              className={styles["top-accordion-details"]}
              aria-description="top accordion details"
            >
              <span
                className={styles["request-accordion-name"]}
                aria-description="request accordion name"
              >
                {request.resource.name}{" "}
              </span>      
              {request.resource.deleted && (
                <span
                  className={
                    request.resource.active === false
                      ? styles["resource-marked-for-deletion"]
                      : styles["resource-deleted"]
                  }
                >
                  {request.resource.active === false
                    ? "(Marked for Deletion)"
                    : "(Deleted)"}
                </span>
              )}
              {tooltipContent && (
                <FontAwesomeIcon
                  size={"lg"}
                  icon={faQuestionCircle}
                  data-tooltip-id={`resource-${request.resource.name}-tooltip-content`}
                  data-tooltip-delay-show={500}
                  aria-description="request toolip icon"
                />
              )}
              {request.resource.previousRevision && request.status !== "APPROVED" && (
                <FontAwesomeIcon
                  size={"lg"}
                  icon={faWrench}
                  data-tooltip-id={`resource-${request.resource.name}-revision-tooltip-content`}
                  data-tooltip-delay-show={500}
                  aria-description="request revision tooltip icon"
                />
              )}
            </div>
            <a
              href={request.resource.url}
              className={styles["request-accordion-url"]}
              aria-description={`${request.resource.name} resource link`}
            >
              {request.resource.url}
            </a>
            <div
              className={styles["request-accordion-status"]}
              aria-description="container for request status"
            >
              <span
                className={styles["request-accordion-current-status"]}
                aria-description="container for request current status"
              >
                {`Status: ${STAGE_MAPPING_MISC[latestTransition].status}`}
              </span>

              <span
                className={styles["request-accordion-progress-bar"]}
                aria-description="container for request progress bar"
              >
                <ProgressBar
                  className={styles["request-progress-bar"]}
                  progressColor={STAGE_MAPPING_MISC[latestTransition].color}
                  totalCompletionLabel=""
                  centeredLabel={true}
                  discreteUnit=""
                  currentMarker={
                    latestTransition
                      ? STAGE_MAPPING_MARKER[latestTransition].id
                      : null
                  }
                  progressMarkers={progressMarkers}
                />
              </span>
              {!lodash.isNull(locked) && (
                <FontAwesomeIcon
                  size={"lg"}
                  icon={locked ? faLock : faLockOpen}
                  data-testid={
                    locked ? "locked-for-editing" : "unlocked-for-editing"
                  }
                  data-tooltip-id={`locked-${request.resource.name}-tooltip-content`}
                  data-tooltip-delay-show={500}
                  aria-checked={locked}
                  aria-description="locked for editing indicator"
                />
              )}
            </div>
          </div>
          <div
            className={styles["accordion-arrow"]}
            aria-checked={open}
            aria-description="accordion header arrow marker"
          >
            <FontAwesomeIcon
              size={"xl"}
              icon={open ? faAngleDown : faAngleRight}
            />
          </div>
        </summary>

        <section
          className={styles["request-accordion-content"]}
          aria-description={`container for ${request.resource.name} accordion content`}
        >
          {children()}
        </section>
      </details>
      {tooltipContent && (
        <Tooltip
          id={`resource-${request.resource.name}-tooltip-content`}
          className={styles["resource-tooltip-content"]}
          place={"right-start"}
        >
          {tooltipContent}
        </Tooltip>
      )}
      {request.resource.previousRevision && (
        <Tooltip
          id={`resource-${request.resource.name}-revision-tooltip-content`}
          className={styles["resource-tooltip-content"]}
          place={"right-start"}
        >
          This is a revision of an existing resource
        </Tooltip>
      )}
      {!lodash.isNull(locked) && (
        <Tooltip
          id={`locked-${request.resource.name}-tooltip-content`}
          className={styles["locked-tooltip-content"]}
          place={"right-start"}
        >
          <b>{request.resource.name}</b>
          {`${
            locked
              ? " - The request for this resource has been submitted and cannot be edited at this time."
              : " - The request for this resource can be edited"
          }`}
        </Tooltip>
      )}
    </>
  );
}
