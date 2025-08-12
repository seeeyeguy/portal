import React from "react";
import numeral from "numeral";

import { IProgramCardProps } from "views/components/ProgramCard/ProgramCard";

import { calculateFontSize } from "views/utils/FontSizeUtility";

import styles from "views/components/ProgramCard/ProgramCard.module.css";

const DEFAULT_FONT_SIZE = "3.4vh";
const FONT_SIZE_SLOPE = 1.2;
const INPUT_CUTOFF = 4;
const MAX_FONT_SIZE = 1.85;
const MIN_FONT_SIZE = 1.1;

export default function ProgramCardCondensed({
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
      className={`${styles["program-card"]} ${styles["condensed"]} ${program?.disabled ? styles["disabled"] : ""} ${program && !program?.activeStatus ? styles["invalid"] : ""}`}
      aria-description="container for program information"
    >
      <input
        type="text"
        value={program?.paNumber ?? inputValue}
        autoFocus={!program}
        disabled={!!program}
        className={`${styles["program-input"]} ${styles["condensed"]}`}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        aria-description="input for pa number"
        style={{ fontSize }}
      />
      <div
        className={`${styles["program-details"]} ${styles["condensed"]} ${!program ? styles["unpopulated-details"] : ""}`}
        aria-description="container for main program details"
      >
        <h3>{program?.name || "Program Name"}</h3>
        <div
          className={styles["right-details"]}
          aria-description="container for extra program details"
        >
          <span
            className={styles["program-value"]}
            aria-description="container for program contract value (in millions)"
          >
            {program?.contractValue
              ? `${numeral(program.contractValue).format("$0.0a").toUpperCase()}`
              : !program?.paNumber && "Value"}
          </span>
          <div
            className={`${styles["tier"]} ${styles["condensed"]} ${program ? styles[`tier-${program.tier || "na"}`] : ""}`}
            aria-description="program tier"
          >
            Tier {program && (program.tier || "NA")}
          </div>
        </div>
      </div>
    </section>
  );
}
