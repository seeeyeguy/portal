import React from "react";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import { Dropdown, DropdownChangeEvent } from "primereact/dropdown";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faQuestionCircle } from "@fortawesome/free-regular-svg-icons";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";

import {
  useGetContentQuery,
  useAddContentMutation,
  useUpdateContentMutation,
  useRemoveContentMutation,
} from "state/query/api/portal/content/ContentApi";
import { useGetReportingPeriodQuery } from "state/query/api/portal/programReviewTool/RecordApi";

import { resolveApiErrorMessage } from "utils/PromiseUtility";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";
import { REPORTING_PERIOD_CONTENT_KEY } from "views/definitions/ProgramReviewTool.types";

import styles from "views/containers/AdminControls/AdminControls.module.css";

// 24 gives a good number of reporting periods allowing a
// full range of selections and number of previous reporting periods.
const NUMBER_OF_REPORTING_PERIODS_TO_RETRIEVE = 24;

// Returns the first half of an array of numbers .
const getFirstHalf = (arr: number[]) => {
  const midpoint = Math.ceil(arr.length / 2);
  return arr.slice(0, midpoint);
};

export default function ReportingPeriodControls() {
  const { data: reportingPeriods = [], isLoading: isLoadingReportingPeriods } =
    useGetReportingPeriodQuery(NUMBER_OF_REPORTING_PERIODS_TO_RETRIEVE);

  const {
    data: reportingPeriodContent,
    isLoading: isLoadingReportingPeriodContent,
    refetch,
  } = useGetContentQuery(REPORTING_PERIOD_CONTENT_KEY);

  const [addContent] = useAddContentMutation();
  const [updateContent] = useUpdateContentMutation();
  const [removeContent] = useRemoveContentMutation();

  const [currentReportingPeriods, setCurrentReportingPeriods] = React.useState<
    number[]
  >([]);

  const [showSaveModal, setShowSaveModal] = React.useState(false);
  const [showClearModal, setShowClearModal] = React.useState(false);

  const [tempReportingPeriods, setTempReportingPeriods] = React.useState(
    currentReportingPeriods
  );

  const [numOfPreviousPeriods, setNumOfPreviousPeriods] =
    React.useState<number>(0);
  const [selectedPeriod, setSelectedPeriod] = React.useState<number | null>();

  // Set current reporting periods when api query returns data.
  React.useEffect(() => {
    if (!reportingPeriodContent?.data) {
      setCurrentReportingPeriods([]);
      return;
    }

    const periods = (
      (
        reportingPeriodContent.data as import("definitions/portal/content/Content.types").IContent
      ).content as Record<string, unknown>
    )["periods"];

    setCurrentReportingPeriods(
      Array.isArray(periods) && periods.length > 0 ? (periods as number[]) : []
    );
  }, [reportingPeriodContent]);

  // When either the api query or the clear method adjusts the current reporting periods, set everything else.
  React.useEffect(() => {
    setTempReportingPeriods(currentReportingPeriods);
    // Prevent value from dropping below 0.
    setNumOfPreviousPeriods(Math.max(0, currentReportingPeriods.length - 1));
    setSelectedPeriod(currentReportingPeriods[0]);
  }, [currentReportingPeriods]);

  // Based on the currently selected period and number of previous periods
  // we can calculate how many and which periods are actually selected.
  const recalculateReportingPeriods = React.useCallback(
    (currentPeriod: number, numPeriods: number) => {
      const newReportingPeriods = [currentPeriod];
      const selectedPeriodIndex = reportingPeriods.indexOf(currentPeriod);

      if (selectedPeriodIndex !== -1) {
        for (let i = 1; i <= numPeriods; i++) {
          if (selectedPeriodIndex + i < reportingPeriods.length) {
            newReportingPeriods.push(reportingPeriods[selectedPeriodIndex + i]);
          }
        }
      }

      return newReportingPeriods;
    },
    [reportingPeriods]
  );

  // Save reporting period value selection.
  const handleSave = React.useCallback(
    async (newReportingPeriods: number[]) => {
      if (newReportingPeriods.length) {
        let response;

        if (!currentReportingPeriods.length) {
          // Key has not been created yet or has been previously cleared.
          response = await addContent({
            key: REPORTING_PERIOD_CONTENT_KEY,
            content: { periods: newReportingPeriods },
          });
        } else {
          // Key exists.
          response = await updateContent({
            body: { content: { periods: newReportingPeriods } },
            key: REPORTING_PERIOD_CONTENT_KEY,
          });
        }

        // Handle the create API error.
        if (response.error) {
          const message =
            "data" in response.error
              ? resolveApiErrorMessage(response.error.data as string | object)
              : DEFAULT_API_ERROR_MESSAGE;

          toast.error(`Error Setting Reporting Periods`);
          console.error(message);
        } else {
          toast.success(`Reporting Periods Set`);
          setShowSaveModal(false);
        }
      }
    },
    [currentReportingPeriods, addContent, updateContent]
  );

  // Reset reporting periods back to the initial values.
  const handleCancel = React.useCallback(() => {
    setSelectedPeriod(currentReportingPeriods[0]);
    setTempReportingPeriods(currentReportingPeriods);
    setNumOfPreviousPeriods(Math.max(0, currentReportingPeriods.length - 1));
    setShowSaveModal(false);
  }, [currentReportingPeriods]);

  // Clear initial reporting period values, so no values are selected.
  const handleClear = React.useCallback(async () => {
    if (currentReportingPeriods.length > 0) {
      // Key has not been created yet or has been previously cleared.
      const response = await removeContent(REPORTING_PERIOD_CONTENT_KEY);

      // Handle the create API error.
      if (response.error) {
        const message =
          "data" in response.error
            ? resolveApiErrorMessage(response.error.data as string | object)
            : DEFAULT_API_ERROR_MESSAGE;

        toast.error(`Error Clearing Reporting Periods`);
        console.error(message);
      } else {
        await refetch();
        setCurrentReportingPeriods([]);
        toast.success(`Reporting Periods Cleared`);
        setShowClearModal(false);
      }
    }
  }, [currentReportingPeriods, removeContent, refetch]);

  // When the number reporting period is changed, adjust list of selected periods.
  const handleCurrentReportingPeriodChange = React.useCallback(
    (event: DropdownChangeEvent) => {
      const newSelectedPeriod = event.value;
      if (newSelectedPeriod) {
        setSelectedPeriod(newSelectedPeriod);
        setTempReportingPeriods(
          recalculateReportingPeriods(newSelectedPeriod, numOfPreviousPeriods)
        );
      }
    },
    [numOfPreviousPeriods, recalculateReportingPeriods]
  );

  // When a current reporting period is changed, adjust list of selected periods.
  const handlePreviousPeriodsChange = React.useCallback(
    (event: DropdownChangeEvent) => {
      const newNumOfPreviousPeriods = event.value;
      if (selectedPeriod) {
        setNumOfPreviousPeriods(newNumOfPreviousPeriods);
        setTempReportingPeriods(
          recalculateReportingPeriods(selectedPeriod, newNumOfPreviousPeriods)
        );
      }
    },
    [selectedPeriod, recalculateReportingPeriods]
  );

  return (
    <>
      {isLoadingReportingPeriods || isLoadingReportingPeriodContent ? (
        <div
          className={styles["admin-loading"]}
          aria-description="container to display when loading initial data"
        >
          <MoonLoader />
        </div>
      ) : (
        <>
          <div
            className={styles["admin-controls"]}
            aria-description="container to employee level controls"
          >
            <button
              className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
              disabled={!selectedPeriod}
              onClick={() => setShowSaveModal(true)}
              aria-label="Save Reporting Periods"
            >
              Save
            </button>

            <button
              className={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
              onClick={() => setShowClearModal(true)}
              disabled={!currentReportingPeriods.length}
              aria-label="Clear Reporting Periods"
            >
              Clear
            </button>

            <button
              className={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
              onClick={() => handleCancel()}
              aria-label="Cancel Changes"
            >
              Cancel
            </button>
          </div>

          <div
            className={styles["admin-controls"]}
            aria-description="container for Reporting Period Controls"
          >
            <Dropdown
              className={styles["reporting-period-dropdown"]}
              value={selectedPeriod}
              // Prevents the user from selecting from the second half of the older periods.
              options={getFirstHalf(reportingPeriods)}
              onChange={handleCurrentReportingPeriodChange}
              placeholder="Current Reporting Period"
              tooltip="Select the current (editable) reporting period"
              tooltipOptions={{ position: "right" }}
            />
            <Dropdown
              value={numOfPreviousPeriods}
              options={[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}
              onChange={handlePreviousPeriodsChange}
              placeholder="Number of Previous Periods"
              tooltip="Select the number of previous (non-editable) periods to be visible"
              tooltipOptions={{ position: "right" }}
            />
            <FontAwesomeIcon
              size={"xl"}
              icon={faQuestionCircle}
              data-tooltip-id={"admin-question-tooltip"}
              data-tooltip-delay-show={500}
              aria-description="admin question tooltip icon"
            />
            <Tooltip
              id={`admin-question-tooltip`}
              className={styles["admin-tooltip-content"]}
              place={"right-start"}
            >
              By default, the Program Performance Form automatically selects the
              most recent reporting period stored in the PMX database (with one
              previous being visible).
              <br />
              <br />
              However, on this page you can manually overwrite that selection,
              choosing any earlier period in the last year and specifying how
              many previous periods should remain visible. This will NOT
              automatically update and will have to be manually changed for the
              next period.
              <br />
              <br />
              Clearing this selection will reset the system back to using the
              automated process.
            </Tooltip>
          </div>
          {tempReportingPeriods.length > 0 && (
            <table
              className={styles["single-column-table"]}
              aria-description="Selected Reporting Periods"
            >
              <tbody>
                {tempReportingPeriods.map((period, index) => (
                  <tr key={period}>
                    <td>
                      {index === 0 ? (
                        <>
                          {period} <strong>&nbsp;&nbsp;(Current)</strong>
                        </>
                      ) : (
                        period
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
      <ConfirmModal
        title="Update Reporting Periods"
        open={showSaveModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Save</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleSave(tempReportingPeriods)}
        onReject={() => handleCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      >
        <div
          className={styles["compare-row"]}
          aria-description="Compare Reporting Periods"
        >
          <div aria-description="Selected Reporting Periods">
            <h4>New Reporting Periods</h4>
            {tempReportingPeriods.length > 0 && (
              <table className={styles["single-column-table"]}>
                <tbody>
                  {tempReportingPeriods.map((period, index) => (
                    <tr key={period}>
                      <td>
                        {index === 0 ? (
                          <>
                            {period} <strong>&nbsp;&nbsp;(Current)</strong>
                          </>
                        ) : (
                          period
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          <div aria-description="Previous Reporting Periods">
            <h4>Previous Reporting Periods</h4>
            {currentReportingPeriods.length > 0 ? (
              <table className={styles["single-column-table"]}>
                <tbody>
                  {currentReportingPeriods.map((period, index) => (
                    <tr key={period}>
                      <td>
                        {index === 0 ? (
                          <>
                            {period} <strong>&nbsp;&nbsp;(Current)</strong>
                          </>
                        ) : (
                          period
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              "None"
            )}
          </div>
        </div>
      </ConfirmModal>
      <ConfirmModal
        title="Remove Manually Set Reporting Periods"
        open={showClearModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Clear</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleClear()}
        onReject={() => setShowClearModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
    </>
  );
}
