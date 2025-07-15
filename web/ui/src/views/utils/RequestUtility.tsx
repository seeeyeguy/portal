import { IDisposition } from "definitions/portal/request/Disposition.types";
import { ITransitionGraph } from "definitions/portal/request/Transition.types";

const DRAFT = 1;

export const tooltipTemplate = (transition: ITransitionGraph): JSX.Element => {
  const revisionPreviousTransition = transition.nodes[transition.latest];

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
        <p>Justification - {justification ?? "N/A"}</p>
      </>
    );
  };

  // Disposition for Previous transition of latest transition.
  const previousTransition = revisionPreviousTransition.previousTransition;
  const previousTransitionDispositions = previousTransition
    ? (transition.nodes[previousTransition].dispositions as IDisposition[])
    : [];

  // Get revision disposition if a revision was requested.
  const isDraftStage = revisionPreviousTransition.stage.level === DRAFT;
  const revisionDispositionPrevious = isDraftStage
    ? revisionPreviousTransition.previousTransition
    : null;
  const revisionDispositionRevisionTransition = revisionDispositionPrevious
    ? transition.nodes[revisionDispositionPrevious].previousTransition
    : null;
  const revisionDisposition = revisionDispositionRevisionTransition
    ? (transition.nodes[revisionDispositionRevisionTransition]
        .dispositions as IDisposition[])
    : [];

  // Determine the disposition to display.
  const dispositionDetails = previousTransitionDispositions.length
    ? getDispositionDetails(previousTransitionDispositions)
    : getDispositionDetails(revisionDisposition);

  return (
    <>
      <p>Current Transition - {revisionPreviousTransition.stage.name}</p>
      {dispositionDetails}
    </>
  );
};
