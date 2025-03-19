import React from "react";

import { IProgram } from "views/definitions/ProgramReviewTool.types";

import styles from "views/components/ProgramCard/ProgramCard.module.css";

/** Properties for the ProgramsCard component. */
export interface IProgramCardProps {
  /** Text input for program name. */
  inputValue?: string;

  /** The program to display on card. */
  program?: IProgram;

  /** Callback to invoke when the program name should be submitted.
   * @param name The name of the program.
   */
  submitProgram?: (name: string) => void;

  /** Callback to set text input for program name.
   * @param value text input to set.
   */
  setInputValue?: (value: string) => void;
}

export default function ProgramCard({
  inputValue,
  program,
  submitProgram,
  setInputValue,
}: IProgramCardProps) {
  const handleInputChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      if (setInputValue) {
        setInputValue((event.target.value as string).toUpperCase());
      }
    },
    [setInputValue]
  );

  const handleKeyDown = React.useCallback(
    (event: React.KeyboardEvent<HTMLInputElement>) => {
      if (setInputValue && submitProgram) {
        if ((event.key === "Enter" || event.key === "Tab") && inputValue) {
          submitProgram(inputValue);
        }
      }
    },
    [inputValue, setInputValue, submitProgram]
  );

  return (
    <section
      className={`${styles["program-card"]} ${program?.disabled ? styles["disabled"] : ""} ${program && !program?.valid ? styles["invalid"] : ""}`}
      aria-description="container for program information"
    >
      <input
        type="text"
        value={program?.paNumber ?? inputValue}
        autoFocus={!program}
        disabled={!!program}
        className={styles["program-input"]}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        aria-description="input for pa number"
      />
      <div
        className={`${styles["program-details"]} ${!program ? styles["unpopulated-details"] : ""}`}
        aria-description="container for program details"
      >
        <header
          className={styles["top-details"]}
          aria-description="container for main program details"
        >
          <h3>{program?.programName || "Program Name"}</h3>
          <span
            className={styles["program-value"]}
            aria-description="container for program contract value (in millions)"
          >
            {program?.contractValue ? `$${program.contractValue}` : "Value"}
          </span>
        </header>
        <div
          className={styles["bottom-details"]}
          aria-description="container for program hierarchy details"
        >
          <div className={styles["program-hierarchy"]}>
            <span
              className={styles["program-sector"]}
              aria-description="container for program sector"
            >
              {program?.sector || "Sector"}
            </span>
            <span
              className={styles["program-division"]}
              aria-description="container for program division"
            >
              {program?.division || "Division"}
            </span>
          </div>
          <div
            className={`${styles["tier"]} ${program ? styles[`tier-${program?.tier || "na"}`] : ""}`}
            aria-description="container for program tier"
          >
            Tier {program && (program?.tier || "NA")}
          </div>
        </div>
      </div>
    </section>
  );
}
