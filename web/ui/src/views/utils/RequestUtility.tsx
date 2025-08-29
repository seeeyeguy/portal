import { IDisposition } from "definitions/portal/request/Disposition.types";
import { IRequest } from "definitions/portal/request/Request.types";

const DRAFT = 1;

export const tooltipTemplate = (request: IRequest): JSX.Element => {
  const revisionPreviousTransition = request.transitions.nodes[request.transitions.latest];

  // Helper function to get the disposition details.
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
        { justification && <p>Justification - {justification ?? "N/A"}</p>}
      </>
    );
  };

  // Disposition for Previous transition of latest transition.
  const previousTransition = revisionPreviousTransition.previousTransition;
  const previousTransitionDispositions = previousTransition
    ? (request.transitions.nodes[previousTransition].dispositions as IDisposition[])
    : [];

  // Get revision disposition if a revision was requested.
  const isDraftStage = revisionPreviousTransition.stage.level === DRAFT;
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

  // Determine the disposition to display.
  const dispositionDetails = previousTransitionDispositions.length
    ? getDispositionDetails(previousTransitionDispositions)
    : getDispositionDetails(revisionDisposition);

  return (
    <>
      <b>{`Submitted by - ${request.originator.user.firstName} ${request.originator.user.lastName}`}</b>
      <p>Current Transition - {revisionPreviousTransition.stage.name}</p>
      {dispositionDetails}
    </>
  );
};
