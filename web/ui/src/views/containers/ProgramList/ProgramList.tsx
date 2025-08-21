import React from "react";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import {
  faAdd,
  faEye,
  faEyeLowVision,
  faTrash,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";

import ProgramCard from "views/components/ProgramCard/ProgramCard";
import ProgramCardCondensed from "views/components/ProgramCard/ProgramCardCondensed";

import store from "state/store/store";
import programApi from "state/query/api/portal/programReviewTool/ProgramApi";

import {
  IProgram,
  IPrograms,
  IPortfolio,
} from "views/definitions/ProgramReviewTool.types";

import styles from "views/containers/ProgramList/ProgramList.module.css";

const MAX_PROGRAMS = 40;

/** Properties for the ProgramList component. */
interface IProgramListProps {
  /** A portfolio of programs to list. */
  portfolio: IPortfolio;

  /** Callback to invoke when the dictionary of programs should be updated.
   * @param portfolioPrograms New dictionary of programs.
   */
  setPortfolioPrograms(portfolioPrograms: IPrograms): void;
}

export default function ProgramsForm({
  portfolio,
  setPortfolioPrograms,
}: IProgramListProps) {
  const [inputValue, setInputValue] = React.useState<string>("");
  const [fetchingProgram, setFetchingProgram] = React.useState(false);

  const handleRemoveProgram = React.useCallback(
    (programId: string) => {
      if (portfolio.programs[programId]) {
        const newPrograms = { ...portfolio.programs };
        delete newPrograms[programId];
        setPortfolioPrograms(newPrograms);
      }
    },
    [portfolio, setPortfolioPrograms]
  );

  const handleDisableProgram = React.useCallback(
    (programId: string) => {
      if (portfolio.programs[programId]) {
        const newPrograms = { ...portfolio.programs };
        newPrograms[programId] = {
          ...newPrograms[programId],
          disabled: !newPrograms[programId].disabled,
        };

        setPortfolioPrograms(newPrograms);
      }
    },
    [portfolio, setPortfolioPrograms]
  );

  const handleAddProgram = React.useCallback(
    async (paNumber: string) => {
      if (!paNumber) {
        return;
      }

      if (
        Object.values(portfolio.programs).some(
          (program) => program.paNumber === paNumber
        )
      ) {
        toast.error(`Program already selected: ${paNumber}`);
        return;
      }

      setFetchingProgram(true);
      const promise = store.dispatch(
        programApi.endpoints.getPrograms.initiate([paNumber])
      );
      const response = await promise;
      setFetchingProgram(false);

      const { data: fetchedProgram } = response?.data ?? { data: [] };
      const retrievedProgram = (fetchedProgram as Record<string, IProgram>)[
        paNumber
      ];

      if (!retrievedProgram) {
        toast.error(`Program not found: ${paNumber}`);
        return;
      }

      const newPortfolioPrograms: IPrograms = {
        ...portfolio.programs,
        ...{ [paNumber]: retrievedProgram },
      };

      setPortfolioPrograms(newPortfolioPrograms);
      setInputValue("");
    },
    [portfolio, setPortfolioPrograms]
  );

  return (
    <>
      <ul
        className={`${styles["program-portfolio-list"]} ${styles["condensed"]}`}
        aria-description="list of programs in portfolio"
      >
        {Object.entries(portfolio.programs || {}).map(([key, program]) => (
          <li key={key} className={styles["program-item"]}>
            <ProgramCardCondensed program={program} />
            <div
              className={styles["program-controls"]}
              aria-description="container for controls of a program"
            >
              <button
                disabled={!program.activeStatus}
                onClick={() => handleDisableProgram(key)}
                aria-description="program control button to disable program"
              >
                <FontAwesomeIcon
                  icon={program.disabled ? faEyeLowVision : faEye}
                />
              </button>
              <button
                onClick={() => handleRemoveProgram(key)}
                aria-description="program control button to remove program"
              >
                <FontAwesomeIcon icon={faTrash} />
              </button>
            </div>
          </li>
        ))}
        {lodash.keys(portfolio?.programs).length < MAX_PROGRAMS && (
          <li className={styles["program-item"]}>
            <ProgramCardCondensed
              submitProgram={handleAddProgram}
              inputValue={inputValue}
              setInputValue={setInputValue}
            />
            <div
              className={styles["program-controls"]}
              aria-description="container for controls of a program"
            >
              {fetchingProgram ? (
                <MoonLoader size={40} />
              ) : (
                <button onClick={() => handleAddProgram(inputValue)}>
                  <FontAwesomeIcon
                    icon={faAdd}
                    aria-description="program control button to add a program"
                  />
                </button>
              )}
            </div>
          </li>
        )}
      </ul>

      <ul
        className={styles["program-portfolio-list"]}
        aria-description="list of programs in portfolio"
      >
        {Object.entries(portfolio?.programs || {}).map(([key, program]) => (
          <li key={key} className={styles["program-item"]}>
            <ProgramCard program={program} />
            <div
              className={styles["program-controls"]}
              aria-description="container for controls of a program"
            >
              <button
                disabled={!program.activeStatus}
                onClick={() => handleDisableProgram(key)}
                aria-description="program control button to disable program"
              >
                <FontAwesomeIcon
                  icon={program.disabled ? faEyeLowVision : faEye}
                />
              </button>
              <button
                onClick={() => handleRemoveProgram(key)}
                aria-description="program control button to remove program"
              >
                <FontAwesomeIcon icon={faTrash} />
              </button>
            </div>
          </li>
        ))}
        {lodash.keys(portfolio?.programs).length < MAX_PROGRAMS && (
          <li className={styles["program-item"]}>
            <ProgramCard
              submitProgram={handleAddProgram}
              inputValue={inputValue}
              setInputValue={setInputValue}
            />
            <div
              className={styles["program-controls"]}
              aria-description="container for controls of a program"
            >
              {fetchingProgram ? (
                <MoonLoader size={40} />
              ) : (
                <button
                  onClick={() => handleAddProgram(inputValue)}
                  aria-description="program control button to add a program"
                >
                  <FontAwesomeIcon icon={faAdd} />
                </button>
              )}
            </div>
          </li>
        )}
      </ul>
    </>
  );
}
