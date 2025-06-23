import React from "react";
import lodash from "lodash";
import { ProgressBar } from "primereact/progressbar";

import styles from "views/components/ProgressBar/ProgressBar.module.css";

export interface IProgressMarker {
  id: number;
  name?: string;
  complete: boolean;
  completeLabel?: string;
  incompleteLabel?: string;
}

/** Properties for the ProgressBar component. */
export interface IProgressBarProps {
  /** Class selector for the ProgressBar. */
  className?: string;

  /** Array of Progress Markers to define progress. */
  progressMarkers: IProgressMarker[];

  /** When defined, converts displayed progress to discrete increments of the specified progress unit. */
  discreteUnit?: string;

  /** The label to use when progress is 100% complete. */
  totalCompletionLabel?: string;

  /** The default label to use when the current marker is complete. */
  markerCompleteLabel?: string;

  /** The default label to use when the current marker is incomplete. */
  markerIncompleteLabel?: string;

  /** The id of the current progress marker. */
  currentMarker?: number | null;

  /** Custom color for the progress bar. */
  progressColor?: string;

  /** Custom color for the progress bar label. */
  progressLabelColor?: string;

  /** Show progress value. */
  showValue?: boolean;

  /** Enable diagonal striped styling. */
  striped?: boolean;

  /** Enable label to appear in center of bar regardless of value. */
  centeredLabel?: boolean;
}

const MAX_PERCENTAGE_VALUE = 100;

export default function IProgressBar({
  className,
  progressMarkers,
  discreteUnit,
  showValue = true,
  striped = false,
  centeredLabel = false,
  currentMarker,
  totalCompletionLabel = "Completed",
  markerCompleteLabel = "Complete",
  markerIncompleteLabel = "In Progress",
  progressColor,
  progressLabelColor,
}: IProgressBarProps) {
  // Memoized value to calculate the total number of markers.
  const totalMarkers = React.useMemo(
    () => progressMarkers.length,
    [progressMarkers]
  );

  // Memoized value to calculate the number of completed markers.
  const completedMarkers = React.useMemo(
    () => progressMarkers.filter((marker) => marker.complete).length,
    [progressMarkers]
  );

  // Memoized value of the current progress as a percentage.
  const currentProgress = React.useMemo(
    () => Math.round((completedMarkers / totalMarkers) * MAX_PERCENTAGE_VALUE),
    [completedMarkers, totalMarkers]
  );

  // Find the current marker by ID.
  const currentProgressMarker = React.useMemo(
    () => progressMarkers.find((marker) => marker.id === currentMarker),
    [progressMarkers, currentMarker]
  );

  // Handles the displaying of progress bar label increments in discrete amounts.
  const discreteTemplate = () => {
    // EX: "3/4 Steps".
    const completionState = `${completedMarkers}/${totalMarkers} ${discreteUnit}`;

    let progressLabel: string = "";
    if (currentProgress === MAX_PERCENTAGE_VALUE && totalCompletionLabel) {
      // EX: "Completed".
      progressLabel = totalCompletionLabel;
    } else if (currentProgressMarker) {
      // EX: "Request - In Progress".
      const labelArray = [
        currentProgressMarker?.name,
        currentProgressMarker?.complete
          ? (currentProgressMarker.completeLabel ?? markerCompleteLabel)
          : (currentProgressMarker.incompleteLabel ?? markerIncompleteLabel),
      ];

      // Removes any falsy strings before joining them.
      progressLabel = labelArray.filter((label) => label).join(" - ");
    }

    return (
      <div
        className={styles["progress-bar-label"]}
        aria-description="container for progress bar label"
        style={
          {
            "--progress-bar-color": progressColor,
            "--progress-bar-label-color": progressLabelColor,
          } as React.CSSProperties
        }
      >
        <span aria-description="container for the completion state of the progress bar">
          {completionState}
        </span>
        {progressLabel.length ? (
          <span
            className={styles["progress-bar-stage-label"]}
            aria-description="container for the progress marker stage label"
          >
            {`| ${progressLabel}`}
          </span>
        ) : (
          <></>
        )}
      </div>
    );
  };

  return (
    <div
      className={`
        ${styles["progress-bar"]} 
        ${currentProgress === 0 && !lodash.isUndefined(discreteUnit) ? styles["progress-bar-empty"] : ""} 
        ${striped ? styles["progress-bar-apply-striped"] : ""} 
        ${className ?? ""}
      `}
      aria-description="container for progress bar"
      style={
        {
          "--progress-bar-color": progressColor,
          "--progress-bar-label-color": progressLabelColor,
        } as React.CSSProperties
      }
    >
      {centeredLabel && (
        <div
          className={styles["progress-bar-center-label"]}
          aria-description="progress bar label"
          style={
            {
              "--progress-bar-label-color": progressLabelColor,
            } as React.CSSProperties
          }
        >
          {!lodash.isUndefined(discreteUnit)
            ? discreteTemplate()
            : `${currentProgress}%`}
        </div>
      )}

      <ProgressBar
        value={
          currentProgress === 0 && !lodash.isUndefined(discreteUnit)
            ? MAX_PERCENTAGE_VALUE
            : currentProgress
        }
        displayValueTemplate={
          !lodash.isUndefined(discreteUnit) && !centeredLabel
            ? discreteTemplate
            : undefined
        }
        showValue={showValue && !centeredLabel}
      ></ProgressBar>
    </div>
  );
}
