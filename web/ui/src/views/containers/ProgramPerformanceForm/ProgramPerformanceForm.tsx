import React from "react";
import { Tooltip } from "react-tooltip";
import lodash from "lodash";
import numeral from "numeral";
import { Dropdown } from "primereact/dropdown";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import {
  IRecord,
  assessmentOptions,
} from "views/definitions/ProgramReviewTool.types";

import styles from "views/containers/ProgramPerformanceForm/ProgramPerformanceForm.module.css";

const assessmentOptionsDropdown = [
  { label: "1 - Red", value: assessmentOptions.RED },
  { label: "2 - Yellow", value: assessmentOptions.YELLOW },
  { label: "3 - Green", value: assessmentOptions.GREEN },
  { label: "4 - Blue", value: assessmentOptions.BLUE },
];

interface ProgramPerformanceFormProps {
  selectedPA: string | null;
  record: IRecord | null;
  isEditable: boolean | null;
}

export default function ProgramPerformanceForm({
  selectedPA,
  record,
  isEditable = false,
}: ProgramPerformanceFormProps) {
  const [formData, setFormData] = React.useState<IRecord | null>(null);
  const [isEditing, setIsEditing] = React.useState<boolean>(
    isEditable ?? false
  );

  const FloatingBoxTooltipContent = ({
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

  const AssessmentTooltipContent = (
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

  const getIndexClass = (value: number | undefined | null) => {
    if (!lodash.isNumber(value)) return styles["finance-metric-box-grey"];

    if (value > 1.0) {
      return styles["finance-metric-box-blue"];
    } else if (value > 0.95 && value <= 1.0) {
      return styles["finance-metric-box-green"];
    } else if (value > 0.9 && value <= 0.95) {
      return styles["finance-metric-box-yellow"];
    } else {
      return styles["finance-metric-box-red"];
    }
  };

  const handleSubmit = React.useCallback(
    (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();

      if (!selectedPA) {
        console.error("Validation failed: PA must be selected.");
        return;
      }

      if (!formData) {
        console.error("Validation failed: Form data is missing.");
        return;
      }

      // Required text fields.

      if (!formData.programPhase?.trim()?.length) {
        console.error("Validation failed: Program Phase is required.");
        return;
      }

      if (!formData.site?.trim()?.length) {
        console.error("Validation failed: Site is required.");
        return;
      }

      if (
        !formData.earnedValueManagementSystemReportingRequirement?.trim()
          ?.length
      ) {
        console.error(
          "Validation failed: EVMS Reporting Requirement is required."
        );
        return;
      }

      // Required assessments.

      if (
        formData.customerAssessment === null ||
        formData.technicalAssessment === null ||
        formData.riskAssessment === null ||
        formData.overallProgram === null
      ) {
        console.error(
          "Validation failed: All subjective assessments must be selected."
        );
        return;
      }

      setIsEditing(false);
    },
    [formData, selectedPA]
  );

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFormData(record); // reset to original data if canceled.
  };

  const tooltipDelayShow = 200;

  React.useEffect(() => {
    setFormData(record);
  }, [record]);

  return (
    <form className="program-record-content" onSubmit={handleSubmit}>
      <div
        className={styles["program-metadata-section"]}
        aria-description="container for program meta data"
      >
        <div
          className={styles["flex-row-group"]}
          aria-description="group container for tier, edit controls, PA, and program details"
        >
          <div
            className={`${styles["tier"]} ${formData ? styles[`tier-${formData?.tier || "NA"}`] : ""}`}
            aria-description="container for program tier"
          >
            Tier {formData && (formData?.tier || "NA")}
          </div>
          {!isEditing ? (
            <button
              type="button"
              className={styles["form-edit-button"]}
              onClick={handleEdit}
            >
              Edit
            </button>
          ) : (
            <button
              type="button"
              className={styles["form-edit-button"]}
              onClick={handleCancel}
            >
              Cancel
            </button>
          )}

          <div
            className={styles["pa-label-large"]}
            aria-description="program PA display"
          >
            {selectedPA}
          </div>
          <div
            className={styles["vertical-divider-red"]}
            aria-description="visual separator"
          ></div>
          <div
            className={styles["field-pair"]}
            aria-description="container for sector and division information"
          >
            <h3 className={styles["field-label"]}>Sector:</h3>
            <p className={styles["field-value"]}>{formData?.sector || "-"}</p>
            <h3 className={styles["field-label"]}>Division:</h3>
            <p className={styles["field-value"]}>{formData?.division || "-"}</p>
          </div>
          <div
            className={styles["field-pair"]}
            aria-description="container for program manager and financial analyst information"
          >
            <h3 className={styles["field-label"]}>Program Manager:</h3>
            <p className={styles["field-value"]}>
              -{/* {formData?.programManager.join(", ") || "-"} */}
            </p>
            <h3 className={styles["field-label"]}>
              Program Financial Analyst:
            </h3>
            <p className={styles["field-value"]}>
              -{/* {formData?.programFinancialAnalyst.join(", ") || "-"} */}
            </p>
          </div>
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
                className={styles["field-text-input"]}
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
                className={styles["field-text-input"]}
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
                className={styles["field-text-input"]}
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
              className={styles["field-value"]}
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
              <label className={styles["radio-margin-left"]}>
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
              className={styles["field-value"]}
              aria-description="displays selected CSDR clause value"
            >
              <label>
                <input
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
              <label className={styles["radio-margin-left"]}>
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
            data-tooltip-delay-show={tooltipDelayShow}
          >
            <div
              className={`${styles["floating-box"]} ${getIndexClass(
                formData?.schedulePerformanceIndexCumulative
              )}`}
            >
              <span className={styles["floating-label"]}>SPI</span>
              <span className={styles["floating-value"]}>
                {!lodash.isNil(formData?.schedulePerformanceIndexCumulative)
                  ? formData.schedulePerformanceIndexCumulative.toFixed(2)
                  : "-"}
              </span>

              <Tooltip
                id="spi-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
              >
                <strong>Schedule Performance Index (SPI)</strong>
                <div className={styles["tooltip-description-list"]}>
                  {FloatingBoxTooltipContent({
                    type: "SPI",
                    denominator: "BCWS",
                  })}
                </div>
              </Tooltip>
            </div>
          </span>

          {/* CPI. */}
          <span
            data-tooltip-id="cpi-tooltip"
            data-tooltip-delay-show={tooltipDelayShow}
          >
            <div
              className={`${styles["floating-box"]} ${getIndexClass(
                formData?.costPerformanceIndexCumulative
              )}`}
            >
              <span className={styles["floating-label"]}>CPI</span>
              <span className={styles["floating-value"]}>
                {!lodash.isNil(formData?.costPerformanceIndexCumulative)
                  ? formData.costPerformanceIndexCumulative.toFixed(2)
                  : "-"}
              </span>

              <Tooltip
                id="cpi-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
              >
                <strong>Cost Performance Index (CPI)</strong>
                <div className={styles["tooltip-description-list"]}>
                  {FloatingBoxTooltipContent({
                    type: "CPI",
                    denominator: "ACWP",
                  })}
                </div>
              </Tooltip>
            </div>
          </span>
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
            <p className={styles["field-value"]}>
              {formData?.budgetedCostWorkScheduledCumulative
                ? numeral(formData?.budgetedCostWorkScheduledCumulative)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="EAC container"
          >
            <h3 className={styles["field-label"]}>EAC:</h3>
            <p className={styles["field-value"]}>
              {formData?.estimateAtComplete
                ? numeral(formData?.estimateAtComplete)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="BCWP container"
          >
            <h3 className={styles["field-label"]}>BCWP:</h3>
            <p className={styles["field-value"]}>
              {formData?.budgetedCostWorkPerformedCumulative
                ? numeral(formData?.budgetedCostWorkPerformedCumulative)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="ETC container"
          >
            <h3 className={styles["field-label"]}>ETC:</h3>
            <p className={styles["field-value"]}>
              {formData?.estimateToComplete
                ? numeral(formData?.estimateToComplete)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="ACWP container"
          >
            <h3 className={styles["field-label"]}>ACWP:</h3>
            <p className={styles["field-value"]}>
              {formData?.actualCostWorkPerformedCumulative
                ? numeral(formData?.actualCostWorkPerformedCumulative)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="BCWS container"
          >
            <h3 className={styles["field-label"]}>Management Reserve:</h3>
            <p className={styles["field-value"]}>
              {formData?.managementReserve
                ? numeral(formData?.managementReserve)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
          </div>

          <div
            className={styles["two-column-field"]}
            aria-description="BAC container"
          >
            <h3 className={styles["field-label"]}>BAC:</h3>
            <p className={styles["field-value"]}>
              {formData?.budgetAtComplete
                ? numeral(formData?.budgetAtComplete)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
          </div>
          <div
            className={styles["two-column-field"]}
            aria-description="weighted r/o container"
          >
            <h3 className={styles["field-label"]}>Weighted R/O:</h3>
            <p className={styles["field-value"]}>
              {formData?.weightedRisksAndOpportunities
                ? numeral(formData?.weightedRisksAndOpportunities)
                    .format("$0,0")
                    .toUpperCase()
                : "-"}
            </p>
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
                className={getDropdownClass(formData?.customerAssessment)}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="customer-assessment-tooltip"
                data-tooltip-delay-show={tooltipDelayShow}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="customer-assessment-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
              >
                <strong>Customer Assessment:</strong>
                {AssessmentTooltipContent(
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
                className={getDropdownClass(formData?.technicalAssessment)}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="technical-assessment-tooltip"
                data-tooltip-delay-show={tooltipDelayShow}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="technical-assessment-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
              >
                <strong>Technical Assessment:</strong>
                {AssessmentTooltipContent(
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
                className={getDropdownClass(formData?.riskAssessment)}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="risk-assessment-tooltip"
                data-tooltip-delay-show={tooltipDelayShow}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="risk-assessment-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
              >
                <strong>Risk Assessment:</strong>
                {AssessmentTooltipContent(
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
                className={getDropdownClass(formData?.overallProgram)}
                disabled={!isEditing}
              />
              <span
                className={styles["tooltip-icon"]}
                data-tooltip-id="overall-program-assessment-tooltip"
                data-tooltip-delay-show={tooltipDelayShow}
              >
                <FontAwesomeIcon icon={faCircleInfo} />
              </span>
              <Tooltip
                id="overall-program-assessment-tooltip"
                place="left"
                className={styles["program-performance-form-tooltip"]}
              >
                <strong>Overall Program Assessment:</strong>
                {AssessmentTooltipContent(
                  "Significant cost, schedule, technical, and/or customer issues exist",
                  "Moderate cost, schedule, technical, and/or customer issues exist",
                  "Meets cost, schedule, technical, and/or customer expectations",
                  "Exceeds cost, schedule, technical, and/or customer expectations"
                )}
              </Tooltip>
            </div>
          </div>
        </div>

        {/* Comments Section. */}
        <div
          className={styles["single-column-grid"]}
          aria-description="container for comments section"
        >
          <div
            className={styles["item-one"]}
            aria-description="program comments container"
          >
            <h3 className={styles["field-label"]}>Comments:</h3>
            {isEditing ? (
              <textarea
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
              <p className={styles["field-value"]}>
                {formData?.comments || "-"}
              </p>
            )}
          </div>
        </div>
      </div>

      <button className={styles["form-submit-button"]}>Submit</button>
    </form>
  );
}
