import React from "react";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import numeral from "numeral";
import { Dropdown } from "primereact/dropdown";
import { InputNumber } from "primereact/inputnumber";
import { InputTextarea } from "primereact/inputtextarea";

import TaskManager from "views/components/TaskManager/TaskManager";

import recordApi, {
  TApiPostRecordRequest,
  TApiPostRecordTaskRequest,
} from "state/query/api/portal/programReviewTool/RecordApi";
import store from "state/store/store";

import { searchForEmployees } from "services/auth/ldapService";

import {
  assessmentOptions,
  IRecord,
  ITask,
} from "views/definitions/ProgramReviewTool.types";

import styles from "views/containers/ProgramPerformanceForm/ProgramPerformanceForm.module.css";

const TOOLTIP_DELAY_SHOW = 200;

const PROGRAM_MANAGER_ROLE_ID = 1;
const FINANCIAL_ANALYST_ROLE_ID = 2;

const assessmentOptionsDropdown = [
  { label: "1 - Red", value: assessmentOptions.RED },
  { label: "2 - Yellow", value: assessmentOptions.YELLOW },
  { label: "3 - Green", value: assessmentOptions.GREEN },
  { label: "4 - Blue", value: assessmentOptions.BLUE },
];

interface ProgramPerformanceFormProps {
  record: IRecord | null;
  isEditing: boolean | null;
  handleEdit: (value: boolean) => void;
}

export default function ProgramPerformanceForm({
  record,
  isEditing = false,
  handleEdit,
}: ProgramPerformanceFormProps) {
  const [formData, setFormData] = React.useState<IRecord | null>(record);
  const [submittingRecord, setSubmittingRecord] = React.useState(false);
  const [errors, setErrors] = React.useState<
    Record<string, string | Record<number, string[]>>
  >({});

  React.useEffect(() => {
    setFormData(record);
  }, [record]);

  const classifiedSpi: number | string = React.useMemo(
    () =>
      formData?.budgetedCostWorkPerformedCumulative &&
      formData?.budgetedCostWorkScheduledCumulative
        ? (
            formData?.budgetedCostWorkPerformedCumulative /
            formData?.budgetedCostWorkScheduledCumulative
          ).toFixed(2)
        : "-",
    [
      formData?.budgetedCostWorkPerformedCumulative,
      formData?.budgetedCostWorkScheduledCumulative,
    ]
  );

  const classifiedCpi: number | string = React.useMemo(
    () =>
      formData?.budgetedCostWorkPerformedCumulative &&
      formData?.actualCostWorkPerformedCumulative
        ? (
            formData?.budgetedCostWorkPerformedCumulative /
            formData?.actualCostWorkPerformedCumulative
          ).toFixed(2)
        : "-",
    [
      formData?.budgetedCostWorkPerformedCumulative,
      formData?.actualCostWorkPerformedCumulative,
    ]
  );

  const redIndicators: string[] = React.useMemo(() => {
    if (!formData) return [];

    const programIssues: string[] = [];
    if (
      // Ignore if these values are null or undefined.
      !lodash.isNil(formData?.budgetedCostWorkPerformedCumulative) &&
      !lodash.isNil(formData?.budgetAtComplete) &&
      !lodash.isNil(formData?.estimateToComplete) &&
      !lodash.isNil(formData?.estimateAtComplete) &&
      // Ignore programs over 95% complete and less then 7% cost overrun.
      formData.budgetedCostWorkPerformedCumulative / formData.budgetAtComplete <
        0.95 &&
      formData.estimateToComplete > 0.07 * formData.estimateAtComplete
    ) {
      // Indicator 1.
      if (
        !lodash.isNil(formData.costPerformanceIndexCumulative) &&
        formData.costPerformanceIndexCumulative < 0.9
      ) {
        programIssues.push("CPI (CPI < 0.9)");
      }

      // Indicator 2.
      if (
        !lodash.isNil(formData.schedulePerformanceIndexCumulative) &&
        formData.schedulePerformanceIndexCumulative < 0.9
      ) {
        programIssues.push("SPI (SPI < 0.9)");
      }

      // Indicator 3.
      if (formData.estimateAtComplete > 1.1 * formData.budgetAtComplete) {
        programIssues.push("EAC Growth (EAC > BAC by 10%)");
      }

      // Indicator 4.
      if (
        !lodash.isNil(formData.contractEndDate) &&
        formData.estimateAtComplete > 1.1 * formData.budgetAtComplete &&
        new Date().toISOString().split("T")[0] > formData.contractEndDate
      ) {
        programIssues.push("Past Period of Performance");
      }

      // Indicator 5.
      if (
        !lodash.isNil(formData.contractValue) &&
        formData.estimateAtComplete > formData.contractValue
      ) {
        programIssues.push("Over Target Cost (EAC > CV)");
      }
    }

    // Indicator 6.
    if (formData?.overallProgram === 1) {
      programIssues.push("Overall Program Assessment");
    }

    return programIssues;
  }, [formData]);

  const handleTaskChange = React.useCallback((newTasks: ITask[]) => {
    setFormData((prev) => {
      if (!prev) return null;
      if (lodash.isEqual(prev.tasks, newTasks)) return prev;

      return { ...prev, tasks: newTasks };
    });
  }, []);

  const IndexTooltipTemplate = ({
    type,
    denominator,
  }: {
    type: "SPI" | "CPI";
    denominator: "BCWS" | "ACWP";
  }) => {
    return (
      <table className={styles["tooltip-table"]}>
        <tbody>
          <tr>
            <td rowSpan={4}>
              <em>
                {type} = BCWP / {denominator}
              </em>
            </td>
            <td className={`${styles.blue} ${styles["range-cell"]}`}>
              {type} &gt; 1.00
            </td>
          </tr>
          <tr>
            <td className={`${styles.green} ${styles["range-cell"]}`}>
              0.95 &lt; {type} ≤ 1.00
            </td>
          </tr>
          <tr>
            <td className={`${styles.yellow} ${styles["range-cell"]}`}>
              0.90 &lt; {type} ≤ 0.95
            </td>
          </tr>
          <tr>
            <td className={`${styles.red} ${styles["range-cell"]}`}>
              {type} ≤ 0.90
            </td>
          </tr>
        </tbody>
      </table>
    );
  };

  const AssessmentTooltipTemplate = (
    value1: string,
    value2: string,
    value3: string,
    value4: string
  ) => {
    return (
      <div className={styles["tooltip-description-list"]}>
        <div>
          • 1 - <span className={styles["red-font"]}>Red</span>: {value1}
        </div>
        <div>
          • 2 - <span className={styles["yellow-font"]}>Yellow</span>: {value2}
        </div>
        <div>
          • 3 - <span className={styles["green-font"]}>Green</span>: {value3}
        </div>
        <div>
          • 4 - <span className={styles["blue-font"]}>Blue</span>: {value4}
        </div>
      </div>
    );
  };

  const getDropdownClass = (value: assessmentOptions | null | undefined) => {
    switch (value) {
      case assessmentOptions.BLUE:
        return styles["dropdown-blue"];
      case assessmentOptions.GREEN:
        return styles["dropdown-green"];
      case assessmentOptions.YELLOW:
        return styles["dropdown-yellow"];
      case assessmentOptions.RED:
        return styles["dropdown-red"];
      default:
        return "";
    }
  };

  const getIndexClass = (value: number | string | undefined | null) => {
    const numberValue = lodash.toNumber(value);

    if (!lodash.isFinite(numberValue) || lodash.isNaN(numberValue))
      return styles["finance-metric-box-grey"];

    if (numberValue > 1.0) {
      return styles["finance-metric-box-blue"];
    } else if (numberValue > 0.95 && numberValue <= 1.0) {
      return styles["finance-metric-box-green"];
    } else if (numberValue > 0.9 && numberValue <= 0.95) {
      return styles["finance-metric-box-yellow"];
    } else {
      return styles["finance-metric-box-red"];
    }
  };

  const validate = async (
    data: IRecord | null
  ): Promise<Record<string, string | Record<number, string[]>>> => {
    const err: Record<string, string | Record<number, string[]>> = {};

    if (!data) return err;

    // ---- required text fields -------------------------------------------------
    if (!data.programPhase?.trim()) {
      err.programPhase = "Program Phase is required.";
    }
    if (!data.site?.trim()) {
      err.site = "Site is required.";
    }
    if (!data.earnedValueManagementSystemReportingRequirement?.trim()) {
      err.earnedValueManagementSystemReportingRequirement =
        "EVMS Reporting Requirement is required.";
    }

    // ---- required radio buttons -------------------------------------------------
    if (lodash.isNil(data.defenseFinancialAcquisitionRegulationClause)) {
      err.defenseFinancialAcquisitionRegulationClause =
        "DFARS Clause has not been selected.";
    }
    if (lodash.isNil(data.costAndSoftwareDataReportingSystemClause)) {
      err.costAndSoftwareDataReportingSystemClause =
        "CSDR Clause has not been selected.";
    }

    // ---- required assessments -------------------------------------------------
    if (data.customerAssessment === null) {
      err.customerAssessment = "Select a Customer assessment.";
    }
    if (data.technicalAssessment === null) {
      err.technicalAssessment = "Select a Technical assessment.";
    }
    if (data.riskAssessment === null) {
      err.riskAssessment = "Select a Risk assessment.";
    }
    if (data.overallProgram === null) {
      err.overallProgram = "Select an Overall Program assessment.";
    }

    const missingOwners: string[] = [];

    if (data.tasks) {
      const taskErrors: Record<number, string[]> = {};

      for (let index = 0; index < data.tasks.length; index++) {
        const task = data.tasks[index];
        const errors: string[] = [];

        if (!task.name?.trim()) {
          errors.push("name");
        }
        if (!task.description?.trim()) {
          errors.push("description");
        }
        if (!task.owner?.trim()) {
          errors.push("owner");
        } else {
          // check owner existence via LDAP service
          const response = await searchForEmployees(task.owner.trim());
          const ownerExists =
            response.data.length === 1 &&
            task.owner.trim().toLowerCase() ===
              response.data[0].email.toLowerCase();

          if (!ownerExists) {
            errors.push("owner");
            missingOwners.push(task.owner.trim());
          }
        }
        if (!task.targetDate) {
          errors.push("targetDate");
        }

        if (errors.length) {
          taskErrors[index] = errors;
        }
      }

      if (Object.keys(taskErrors).length > 0) {
        err.tasks = taskErrors;
      }
    }

    if (missingOwners.length > 0) {
      err.missingOwners = `One or more Tasks owners cannot be found: ${missingOwners}`;
    }

    return err;
  };

  const handleSubmit = React.useCallback(
    async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();

      if (!formData?.paNumber) {
        return;
      }

      if (!formData) {
        toast.error("Validation failed: Form data is missing.");
        return;
      }

      const newErrors = await validate(formData);
      setErrors(newErrors);
      if (Object.values(newErrors).some((msg) => msg)) {
        const errorList = (
          <ul style={{ margin: 0, paddingLeft: "1.2rem" }}>
            {Object.entries(newErrors).map(
              ([field, message]) =>
                message && (
                  <li key={field}>
                    {lodash.isObject(message) ? (
                      <>
                        Tasks missing fields:
                        <ul style={{ margin: 0, paddingLeft: "1.2rem" }}>
                          {Object.entries(message).map(
                            ([taskField, taskError]) =>
                              taskError && (
                                <li key={taskField}>
                                  {taskError
                                    .map((err) => lodash.startCase(err))
                                    .join(", ")}
                                </li>
                              )
                          )}
                        </ul>
                      </>
                    ) : (
                      message
                    )}
                  </li>
                )
            )}
          </ul>
        );

        toast.error(
          <>
            <div>Validation failed, Please correct the highlighted fields:</div>
            {errorList}
          </>
        );
        return;
      }

      const taskBody: TApiPostRecordTaskRequest[] = (formData?.tasks ?? []).map(
        (task) => ({
          id: task.id,
          pa_number: formData?.paNumber ?? "",
          reporting_period: formData?.reportingPeriod as number,
          order: task.order ?? null,
          name: task.name ?? "",
          description: task.description ?? "",
          owner: task.owner ?? "",
          status: task.status ?? "",
          create_date: task.createDate,
          target_date: task.targetDate ?? "",
          complete_date: task.completeDate ?? null,
          archive_date: task.archiveDate ?? null,
        })
      );

      const requestBody: TApiPostRecordRequest = {
        ...(formData as Omit<TApiPostRecordRequest, "tasks">),
        tasks: taskBody,
      };

      setSubmittingRecord(true);
      const promise = store.dispatch(
        recordApi.endpoints.addRecord.initiate(requestBody)
      );
      const response = await promise;
      setSubmittingRecord(false);

      const { error } = response;

      if (error) {
        const errorMsg = "data" in error ? error.data : error;
        toast.error(`Error creating record: ${JSON.stringify(errorMsg)}`);
        return;
      }

      handleEdit(false);
      toast.success("Record Created");
    },
    [formData, handleEdit]
  );

  return (
    <form
      className={styles["program-record-content"]}
      onSubmit={handleSubmit}
      onKeyDown={(e) => {
        // Allow line‑breaks inside a textarea.
        if (
          e.key === "Enter" &&
          (e.target as HTMLElement).tagName !== "TEXTAREA"
        ) {
          // stop the form from submitting.
          e.preventDefault();
        }
      }}
    >
      <div
        className={styles["section-wrapper"]}
        aria-description="container for program meta data"
      >
        <div
          className={`${styles["tier"]} ${formData ? styles[`tier-${formData?.tier || "na"}`] : ""}`}
          aria-description="container for program tier"
        >
          Tier {formData && (formData?.tier || "NA")}
        </div>
        <div
          className={`${styles["flex-row-group"]} ${styles["metadata-wrapper"]} `}
          aria-description="group container for tier, edit controls, PA, and program details"
        >
          <div
            className={styles["pa-label"]}
            data-tooltip-id="red-indicators-tooltip"
            data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
          >
            <div
              className={styles["pa-label-value"]}
              aria-description="program PA display"
            >
              {record?.paNumber}
            </div>
            {redIndicators.length > 0 && (
              <div className={styles["pa-label-warning"]}>RED PROGRAM</div>
            )}
          </div>
          {redIndicators.length > 0 && (
            <Tooltip
              id="red-indicators-tooltip"
              place="right"
              className={styles["program-performance-form-tooltip"]}
            >
              <strong>Red program due to:</strong>
              <ul className={styles["tooltip-description-list"]}>
                {redIndicators.map((indicator, index) => (
                  <li key={index}>{indicator}</li>
                ))}
              </ul>
            </Tooltip>
          )}

          <span className={styles["pa-metadata"]}>
            <div
              className={styles["field-pair"]}
              aria-description="container for sector and division information"
            >
              <h3 className={styles["field-label"]}>Sector:</h3>
              <p className={styles["field-value"]}>{formData?.sector || "-"}</p>
              <h3
                className={`${styles["field-label"]} ${styles["margin-top"]}`}
              >
                Division:
              </h3>
              <p className={styles["field-value"]}>
                {formData?.division || "-"}
              </p>
            </div>
            <div
              className={styles["field-pair"]}
              aria-description="container for program manager and financial analyst information"
            >
              <h3 className={styles["field-label"]}>Program Manager:</h3>
              {formData?.teamMembers
                .filter((member) => member.role.id === PROGRAM_MANAGER_ROLE_ID)
                .map((member, index, array) => (
                  <p key={member.user.id} className={styles["field-value"]}>
                    {`${member.user.firstName} ${member.user.lastName}${index < array.length - 1 ? "," : ""}`}
                  </p>
                )) ?? "-"}
              <h3
                className={`${styles["field-label"]} ${styles["margin-top"]}`}
              >
                Program Financial Analyst:
              </h3>
              {formData?.teamMembers
                .filter(
                  (member) => member.role.id === FINANCIAL_ANALYST_ROLE_ID
                )
                .map((member, index, array) => (
                  <p key={member.user.id} className={styles["field-value"]}>
                    {`${member.user.firstName} ${member.user.lastName}${index < array.length - 1 ? "," : ""}`}
                  </p>
                )) ?? "-"}
            </div>
          </span>
        </div>
      </div>

      <h2 className={styles["section-header"]}>
        Program &amp; Contract Information
      </h2>

      <div
        className={styles["section-wrapper"]}
        aria-description="container for program and contract details"
      >
        <div
          className={styles["two-column-grid"]}
          aria-description="two-column layout container for contract information"
        >
          <div
            className={styles["two-column-field"]}
            aria-description="program name container"
          >
            <h3 className={styles["field-label"]}>Program/Major Project:</h3>
            <p className={styles["field-value"]}>{formData?.name || "-"}</p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="contract number container"
          >
            <h3 className={styles["field-label"]}>Contract Number:</h3>
            <p className={styles["field-value"]}>
              {formData?.contractNumber || "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="program phase container"
          >
            <h3 className={styles["field-label"]}>Program Phase:</h3>
            {isEditing ? (
              <input
                className={`${styles["field-text-input"]} ${errors["programPhase"] ? styles["input-invalid"] : ""}`}
                type="text"
                value={formData?.programPhase || ""}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      programPhase: event?.target?.value,
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.programPhase || "-"}
              </p>
            )}
          </div>

          <div
            className={styles["two-column-field"]}
            aria-description="contract type container"
          >
            <h3 className={styles["field-label"]}>Contract Type:</h3>
            <p className={styles["field-value"]}>
              {formData?.contractType || "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="site container"
          >
            <h3 className={styles["field-label"]}>Site (City/State):</h3>
            {isEditing ? (
              <input
                className={`${styles["field-text-input"]} ${errors["site"] ? styles["input-invalid"] : ""}`}
                type="text"
                value={formData?.site || ""}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      site: event?.target?.value,
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>{formData?.site || "-"}</p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="contract value container"
          >
            <h3 className={styles["field-label"]}>Contract Value:</h3>
            <p className={styles["field-value"]}>
              {formData?.contractValue
                ? numeral(formData?.contractValue).format("$0,0").toUpperCase()
                : "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="EVMS reporting container"
          >
            <h3 className={styles["field-label"]}>
              EVMS Reporting Requirement:
            </h3>
            {isEditing ? (
              <input
                className={`${styles["field-text-input"]} ${errors["earnedValueManagementSystemReportingRequirement"] ? styles["input-invalid"] : ""}`}
                type="text"
                value={
                  formData?.earnedValueManagementSystemReportingRequirement ||
                  ""
                }
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      earnedValueManagementSystemReportingRequirement:
                        event?.target?.value,
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.earnedValueManagementSystemReportingRequirement ||
                  "-"}
              </p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="contract start date container"
          >
            <h3 className={styles["field-label"]}>Contract Start Date:</h3>
            <p className={styles["field-value"]}>
              {formData?.contractStartDate || "-"}
            </p>
          </div>

          <div
            className={styles["two-column-field"]}
            aria-description="DFARS clause container"
          >
            <h3 className={styles["field-label"]}>DFARS Clause:</h3>
            <div
              className={`${styles["field-value"]} ${styles["radio-input"]} ${errors["defenseFinancialAcquisitionRegulationClause"] ? styles["input-invalid"] : ""}`}
              aria-description="displays selected DFARS clause value"
            >
              <label>
                <input
                  type="radio"
                  name="dfarsClause"
                  value="Yes"
                  checked={
                    formData?.defenseFinancialAcquisitionRegulationClause ===
                    true
                  }
                  disabled={!isEditing}
                  onChange={() =>
                    setFormData((prev): IRecord | null => {
                      if (!prev) return null;
                      return {
                        ...prev,
                        defenseFinancialAcquisitionRegulationClause: true,
                      };
                    })
                  }
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="dfarsClause"
                  value="No"
                  checked={
                    formData?.defenseFinancialAcquisitionRegulationClause ===
                    false
                  }
                  disabled={!isEditing}
                  onChange={() =>
                    setFormData((prev): IRecord | null => {
                      if (!prev) return null;
                      return {
                        ...prev,
                        defenseFinancialAcquisitionRegulationClause: false,
                      };
                    })
                  }
                />
                No
              </label>
            </div>
          </div>

          <div
            className={styles["two-column-field"]}
            aria-description="contract start end container"
          >
            <h3 className={styles["field-label"]}>Contract End Date:</h3>
            <p className={styles["field-value"]}>
              {formData?.contractEndDate || "-"}
            </p>
          </div>

          <div
            className={styles["two-column-field"]}
            aria-description="CSDR clause container"
          >
            <h3 className={styles["field-label"]}>CSDR Clause:</h3>
            <div
              className={`${styles["field-value"]} ${styles["radio-input"]} ${errors["costAndSoftwareDataReportingSystemClause"] ? styles["input-invalid"] : ""}`}
              aria-description="displays selected CSDR clause value"
            >
              <label>
                <input
                  className={`${errors["programPhase"] ? styles["input-invalid"] : ""}`}
                  type="radio"
                  name="csdrClause"
                  value="Yes"
                  checked={
                    formData?.costAndSoftwareDataReportingSystemClause === true
                  }
                  disabled={!isEditing}
                  onChange={() =>
                    setFormData((prev): IRecord | null => {
                      if (!prev) return null;
                      return {
                        ...prev,
                        costAndSoftwareDataReportingSystemClause: true,
                      };
                    })
                  }
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="csdrClause"
                  value="No"
                  checked={
                    formData?.costAndSoftwareDataReportingSystemClause === false
                  }
                  disabled={!isEditing}
                  onChange={() =>
                    setFormData((prev): IRecord | null => {
                      if (!prev) return null;
                      return {
                        ...prev,
                        costAndSoftwareDataReportingSystemClause: false,
                      };
                    })
                  }
                />
                No
              </label>
            </div>
          </div>
        </div>
      </div>

      <h2 className={styles["section-header"]}>Current Period Performance</h2>
      <div
        className={styles["section-wrapper"]}
        aria-description="container for performance metrics and SPI/CPI data"
      >
        <div
          className={styles["floating-box-absolute-wrapper"]}
          aria-description="wrapper for floating SPI and CPI performance boxes"
        >
          {/* SPI. */}
          <span
            data-tooltip-id="spi-tooltip"
            data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
          >
            <div
              className={`${styles["floating-box"]} ${getIndexClass(
                record?.isManualMetricsEntry
                  ? classifiedSpi
                  : formData?.schedulePerformanceIndexCumulative
              )}`}
            >
              <span className={styles["floating-label"]}>SPI</span>
              {record?.isManualMetricsEntry ? (
                <span className={styles["floating-value"]}>
                  {classifiedSpi}
                </span>
              ) : (
                <span className={styles["floating-value"]}>
                  {!lodash.isNil(formData?.schedulePerformanceIndexCumulative)
                    ? formData?.schedulePerformanceIndexCumulative.toFixed(2)
                    : "-"}
                </span>
              )}
            </div>
          </span>
          <Tooltip
            id="spi-tooltip"
            place="right"
            className={styles["program-performance-form-tooltip"]}
            opacity={1}
          >
            <strong>Schedule Performance Index (SPI)</strong>
            <div className={styles["tooltip-description-list"]}>
              {IndexTooltipTemplate({
                type: "SPI",
                denominator: "BCWS",
              })}
            </div>
          </Tooltip>

          {/* CPI. */}
          <span
            data-tooltip-id="cpi-tooltip"
            data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
          >
            <div
              className={`${styles["floating-box"]} ${getIndexClass(
                record?.isManualMetricsEntry
                  ? classifiedCpi
                  : formData?.costPerformanceIndexCumulative
              )}`}
            >
              <span className={styles["floating-label"]}>CPI</span>
              {record?.isManualMetricsEntry ? (
                <span className={styles["floating-value"]}>
                  {classifiedCpi}
                </span>
              ) : (
                <span className={styles["floating-value"]}>
                  {!lodash.isNil(formData?.costPerformanceIndexCumulative)
                    ? formData?.costPerformanceIndexCumulative.toFixed(2)
                    : "-"}
                </span>
              )}
            </div>
          </span>
          <Tooltip
            id="cpi-tooltip"
            place="right"
            className={styles["program-performance-form-tooltip"]}
            opacity={1}
          >
            <strong>Cost Performance Index (CPI)</strong>
            <div className={styles["tooltip-description-list"]}>
              {IndexTooltipTemplate({
                type: "CPI",
                denominator: "ACWP",
              })}
            </div>
          </Tooltip>
        </div>

        <div
          className={styles["two-column-grid"]}
          aria-description="two-column container for performance values"
        >
          <div
            className={styles["two-column-field"]}
            aria-description="BCWS container"
          >
            <h3 className={styles["field-label"]}>BCWS:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.budgetedCostWorkScheduledCumulative || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      budgetedCostWorkScheduledCumulative: lodash.toNumber(
                        event?.value
                      ),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.budgetedCostWorkScheduledCumulative
                  ? numeral(formData?.budgetedCostWorkScheduledCumulative)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="EAC container"
          >
            <h3 className={styles["field-label"]}>EAC:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.estimateAtComplete || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      estimateAtComplete: lodash.toNumber(event?.value),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.estimateAtComplete
                  ? numeral(formData?.estimateAtComplete)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="BCWP container"
          >
            <h3 className={styles["field-label"]}>BCWP:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.budgetedCostWorkPerformedCumulative || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      budgetedCostWorkPerformedCumulative: lodash.toNumber(
                        event?.value
                      ),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.budgetedCostWorkPerformedCumulative
                  ? numeral(formData?.budgetedCostWorkPerformedCumulative)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="ETC container"
          >
            <h3 className={styles["field-label"]}>ETC:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.estimateToComplete || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      estimateToComplete: lodash.toNumber(event?.value),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.estimateToComplete
                  ? numeral(formData?.estimateToComplete)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="ACWP container"
          >
            <h3 className={styles["field-label"]}>ACWP:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.actualCostWorkPerformedCumulative || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      actualCostWorkPerformedCumulative: lodash.toNumber(
                        event?.value
                      ),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.actualCostWorkPerformedCumulative
                  ? numeral(formData?.actualCostWorkPerformedCumulative)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="BCWS container"
          >
            <h3 className={styles["field-label"]}>Management Reserve:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.managementReserve || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      managementReserve: lodash.toNumber(event?.value),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.managementReserve
                  ? numeral(formData?.managementReserve)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>

          <div
            className={styles["two-column-field"]}
            aria-description="BAC container"
          >
            <h3 className={styles["field-label"]}>BAC:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.budgetAtComplete || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      budgetAtComplete: lodash.toNumber(event?.value),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.budgetAtComplete
                  ? numeral(formData?.budgetAtComplete)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="weighted r/o container"
          >
            <h3 className={styles["field-label"]}>Weighted R/O:</h3>
            {isEditing && record?.isManualMetricsEntry ? (
              <InputNumber
                prefix="$ "
                className={styles["field-currency-input"]}
                value={formData?.weightedRisksAndOpportunities || null}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      weightedRisksAndOpportunities: lodash.toNumber(
                        event?.value
                      ),
                    };
                  })
                }
              />
            ) : (
              <p className={styles["field-value"]}>
                {formData?.weightedRisksAndOpportunities
                  ? numeral(formData?.weightedRisksAndOpportunities)
                      .format("$0,0")
                      .toUpperCase()
                  : "-"}
              </p>
            )}
          </div>
        </div>
      </div>

      <h2 className={styles["section-header"]}>Subjective Assessments</h2>
      <div
        className={styles["section-wrapper"]}
        aria-description="dropdown-based subjective program assessments container"
      >
        <div
          className={styles["two-column-grid"]}
          aria-description="two-column layout for subjective assessment dropdowns"
        >
          {/* Customer Assessment. */}
          <div
            className={styles["two-column-field"]}
            aria-description="customer assessment dropdown container"
          >
            <h3 className={styles["field-label"]}>Customer:</h3>
            <div
              className={styles["dropdown-with-icon"]}
              aria-description="customer assessment dropdown with tooltip"
            >
              <Dropdown
                value={formData?.customerAssessment ?? null}
                options={assessmentOptionsDropdown}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      customerAssessment: event?.value as assessmentOptions,
                    };
                  })
                }
                placeholder="-"
                className={`${styles["dropdown-assessment"]} ${getDropdownClass(formData?.customerAssessment)} ${errors["customerAssessment"] ? styles["input-invalid"] : ""}`}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="customer-assessment-tooltip"
                data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="customer-assessment-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
                opacity={1}
              >
                <strong>Customer Assessment:</strong>
                {AssessmentTooltipTemplate(
                  "Existing - Difficult; Customer's culture and organization not well understood (e.g. International)",
                  "New Customer - No History",
                  "Existing - Reasonable; No long standing relationship",
                  "Existing - Reasonable; Long standing customer relationship"
                )}
              </Tooltip>
            </div>
          </div>

          {/* Technical Assessment. */}
          <div
            className={styles["two-column-field"]}
            aria-description="technical assessment dropdown container"
          >
            <h3 className={styles["field-label"]}>Technical:</h3>
            <div
              className={styles["dropdown-with-icon"]}
              aria-description="technical assessment dropdown with tooltip"
            >
              <Dropdown
                value={formData?.technicalAssessment ?? null}
                options={assessmentOptionsDropdown}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      technicalAssessment: event?.value as assessmentOptions,
                    };
                  })
                }
                placeholder="-"
                className={`${styles["dropdown-assessment"]} ${getDropdownClass(formData?.technicalAssessment)} ${errors["technicalAssessment"] ? styles["input-invalid"] : ""}`}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="technical-assessment-tooltip"
                data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="technical-assessment-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
                opacity={1}
              >
                <strong>Technical Assessment:</strong>
                {AssessmentTooltipTemplate(
                  "Critical accomplishments not met; Impacting schedule",
                  "Behind schedule on technical accomplishments",
                  "Meets technical accomplishments",
                  "Exceeds; Known technology; History of successful accomplishments or deliveries"
                )}
              </Tooltip>
            </div>
          </div>

          {/* Risk Assessment. */}
          <div
            className={styles["two-column-field"]}
            aria-description="risk assessment dropdown container"
          >
            <h3 className={styles["field-label"]}>Risk:</h3>
            <div
              className={styles["dropdown-with-icon"]}
              aria-description="risk assessment dropdown with tooltip"
            >
              <Dropdown
                value={formData?.riskAssessment ?? null}
                options={assessmentOptionsDropdown}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      riskAssessment: event?.value as assessmentOptions,
                    };
                  })
                }
                placeholder="-"
                className={`${styles["dropdown-assessment"]} ${getDropdownClass(formData?.riskAssessment)} ${errors["riskAssessment"] ? styles["input-invalid"] : ""}`}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="risk-assessment-tooltip"
                data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="risk-assessment-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
                opacity={1}
              >
                <strong>Risk Assessment:</strong>
                {AssessmentTooltipTemplate(
                  "Program Risks have High probability of impacting critical schedule milestones and insufficient MR",
                  "Program Risks have Medium probability and lack sufficient MR",
                  "Program Risks have Low probability and sufficient MR",
                  "No Program Risks and sufficient MR"
                )}
              </Tooltip>
            </div>
          </div>
          {/* Overall Program Assessment. */}
          <div
            className={styles["two-column-field"]}
            aria-description="overall program assessment dropdown container"
          >
            <h3 className={styles["field-label"]}>Overall Program:</h3>
            <div
              className={styles["dropdown-with-icon"]}
              aria-description="overall program assessment dropdown with tooltip"
            >
              <Dropdown
                value={formData?.overallProgram ?? null}
                options={assessmentOptionsDropdown}
                onChange={(event) =>
                  setFormData((prev): IRecord | null => {
                    if (!prev) return null;
                    return {
                      ...prev,
                      overallProgram: event?.value as assessmentOptions,
                    };
                  })
                }
                placeholder="-"
                className={`${styles["dropdown-assessment"]} ${getDropdownClass(formData?.overallProgram)} ${errors["overallProgram"] ? styles["input-invalid"] : ""}`}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="overall-program-assessment-tooltip"
                data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="overall-program-assessment-tooltip"
                place="left"
                className={styles["program-performance-form-tooltip"]}
                opacity={1}
              >
                <strong>Overall Program Assessment:</strong>
                {AssessmentTooltipTemplate(
                  "Significant cost, schedule, technical, and/or customer issues exist",
                  "Moderate cost, schedule, technical, and/or customer issues exist",
                  "Meets cost, schedule, technical, and/or customer expectations",
                  "Exceeds cost, schedule, technical, and/or customer expectations"
                )}
              </Tooltip>
            </div>
          </div>
        </div>

        {/* Comments Section */}

        <h3 className={styles["field-label"]}>Comments:</h3>
        {isEditing ? (
          <InputTextarea
            className={styles["comments-textarea"]}
            value={formData?.comments || ""}
            onChange={(event) =>
              setFormData((prev): IRecord | null => {
                if (!prev) return null;
                return { ...prev, comments: event?.target?.value };
              })
            }
          />
        ) : (
          <p className={`${styles["field-value"]} ${styles["comments-value"]}`}>
            {formData?.comments || "-"}
          </p>
        )}
      </div>
      {(formData?.tasks.length || isEditing || redIndicators.length > 0) && (
        <>
          <h2
            className={`${styles["section-header"]} ${redIndicators.length ? styles["return-to-green"] : ""}`}
          >
            Return to Green Plan <label>Required for all Red Programs</label>
          </h2>
          <div
            className={`${styles["section-wrapper"]} ${styles["no-padding"]} ${redIndicators.length ? styles["return-to-green"] : ""}`}
            aria-description="series of tasks to help the program improve metrics"
          >
            <TaskManager
              key={`${record?.paNumber}-${record?.reportingPeriod}`}
              onTasksChange={handleTaskChange}
              tasks={formData?.tasks ?? []}
              isEditing={isEditing ?? false}
              externalValidationErrors={
                errors["tasks"] as Record<number, string[]>
              }
            />
          </div>
        </>
      )}
      <div
        className={styles["button-container"]}
        aria-description="container for submit button"
      >
        {isEditing && (
          <button
            disabled={submittingRecord}
            className={styles["form-submit-button"]}
            type="submit"
          >
            Submit Record
          </button>
        )}
      </div>
    </form>
  );
}
