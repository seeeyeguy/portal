import React from "react";
import numeral from "numeral";

import { IProgram } from "views/definitions/ProgramReviewTool.types";

import { calculateFontSize } from "views/utils/FontSizeUtility";

import styles from "views/components/ProgramCard/ProgramCard.module.css";

const DEFAULT_FONT_SIZE = "2.8vh";
const FONT_SIZE_SLOPE = 0.52;
const INPUT_CUTOFF = 4;
const MAX_FONT_SIZE = 1.85;
const MIN_FONT_SIZE = 0.8;

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
  const [fontSize, setFontSize] = React.useState(
    calculateFontSize(
      DEFAULT_FONT_SIZE,
      FONT_SIZE_SLOPE,
      INPUT_CUTOFF,
      MAX_FONT_SIZE,
      MIN_FONT_SIZE,
      program?.paNumber ?? inputValue
    )
  );

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

  React.useEffect(() => {
    setFontSize(
      calculateFontSize(
        DEFAULT_FONT_SIZE,
        FONT_SIZE_SLOPE,
        INPUT_CUTOFF,
        MAX_FONT_SIZE,
        MIN_FONT_SIZE,
        program?.paNumber ?? inputValue
      )
    );
  }, [inputValue, program?.paNumber]);

  return (
    <section
      className={`${styles["program-card"]} ${program?.disabled ? styles["disabled"] : ""} ${program && !program?.activeStatus ? styles["invalid"] : ""}`}
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
        style={{ fontSize }}
      />
      <div
        className={`${styles["program-details"]} ${!program ? styles["unpopulated-details"] : ""}`}
        aria-description="container for program details"
      >
        <header
          className={styles["top-details"]}
          aria-description="container for main program details"
        >
          <h3>{program?.name || "Program Name"}</h3>
          <span
            className={styles["program-value"]}
            aria-description="container for program contract value (in millions)"
          >
            {program?.contractValue
              ? `${numeral(program.contractValue).format("$0.0a").toUpperCase()}`
              : "Contract Value"}
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
