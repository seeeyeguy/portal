import React from "react";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import lodash from "lodash";
import numeral from "numeral";
import { Dropdown } from "primereact/dropdown";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import recordApi, {
  TApiPostRecordRequest,
} from "state/query/api/portal/programReviewTool/RecordApi";
import store from "state/store/store";

import {
  IRecord,
  assessmentOptions,
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
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  React.useEffect(() => {
    setFormData(record);
  }, [record]);

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

  const validate = (data: IRecord | null): Record<string, string> => {
    const err: Record<string, string> = {};

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

      const newErrors = validate(formData);
      setErrors(newErrors);
      if (Object.values(newErrors).some((msg) => msg)) {
        const errorList = (
          <ul style={{ margin: 0, paddingLeft: "1.2rem" }}>
            {Object.entries(newErrors).map(
              ([field, message]) => message && <li key={field}>{message}</li>
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

      const requestBody: TApiPostRecordRequest = {
        ...(formData as TApiPostRecordRequest),
      };

      setSubmittingRecord(true);
      const promise = store.dispatch(
        recordApi.endpoints.addRecord.initiate(requestBody)
      );
      const response = await promise;
      setSubmittingRecord(false);

      const { error } = response;

      if (error) {
        toast.error(`Error creating record: ${error}`);
        return;
      }

      handleEdit(false);
      toast.success("Record Created");
    },
    [formData, handleEdit]
  );

  return (
    <form className="program-record-content" onSubmit={handleSubmit}>
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
            className={styles["pa-label-large"]}
            aria-description="program PA display"
          >
            {record?.paNumber}
          </div>
          <span className={styles["pa-metadata"]}>
            <div
              className={styles["field-pair"]}
              aria-description="container for sector and division information"
            >
              <h3 className={styles["field-label"]}>Sector:</h3>
              <p className={styles["field-value"]}>{formData?.sector || "-"}</p>
              <h3 className={styles["field-label"]}>Division:</h3>
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
              <h3 className={styles["field-label"]}>
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
                formData?.schedulePerformanceIndexCumulative
              )}`}
            >
              <span className={styles["floating-label"]}>SPI</span>
              <span className={styles["floating-value"]}>
                {!lodash.isNil(formData?.schedulePerformanceIndexCumulative)
                  ? formData?.schedulePerformanceIndexCumulative.toFixed(2)
                  : "-"}
              </span>

              <Tooltip
                id="spi-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
              >
                <strong>Schedule Performance Index (SPI)</strong>
                <div className={styles["tooltip-description-list"]}>
                  {IndexTooltipTemplate({
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
            data-tooltip-delay-show={TOOLTIP_DELAY_SHOW}
          >
            <div
              className={`${styles["floating-box"]} ${getIndexClass(
                formData?.costPerformanceIndexCumulative
              )}`}
            >
              <span className={styles["floating-label"]}>CPI</span>
              <span className={styles["floating-value"]}>
                {!lodash.isNil(formData?.costPerformanceIndexCumulative)
                  ? formData?.costPerformanceIndexCumulative.toFixed(2)
                  : "-"}
              </span>

              <Tooltip
                id="cpi-tooltip"
                place="right"
                className={styles["program-performance-form-tooltip"]}
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
          <p className={styles["field-value"]}>{formData?.comments || "-"}</p>
        )}
      </div>
      <div
        className={styles["button-container"]}
        aria-description="container for submit button"
      >
        {isEditing && (
          <button
            disabled={submittingRecord}
            className={styles["form-submit-button"]}
          >
            Submit Record
          </button>
        )}
      </div>
    </form>
  );
}
