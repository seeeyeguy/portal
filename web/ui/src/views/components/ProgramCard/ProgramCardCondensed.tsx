import React from "react";

import { IProgramCardProps } from "views/components/ProgramCard/ProgramCard";

import styles from "views/components/ProgramCard/ProgramCard.module.css";

export default function ProgramCardCondensed({
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
      className={`${styles["program-card"]} ${styles["condensed"]} ${program?.disabled ? styles["disabled"] : ""} ${program && !program?.valid ? styles["invalid"] : ""}`}
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
      />
      <div
        className={`${styles["program-details"]} ${styles["condensed"]} ${!program ? styles["unpopulated-details"] : ""}`}
        aria-description="container for main program details"
      >
        <h3>{program?.programName || "Program Name"}</h3>
        <div
          className={styles["right-details"]}
          aria-description="container for extra program details"
        >
          <span
            className={styles["program-value"]}
            aria-description="container for program contract value (in millions)"
          >
            {program?.contractValue ? `$${program.contractValue}` : "Value"}
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
