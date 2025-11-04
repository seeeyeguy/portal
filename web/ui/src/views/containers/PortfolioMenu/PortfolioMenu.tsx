import React from "react";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { Tooltip } from "react-tooltip";
import {
  faPlusSquare,
  faSave,
  faTrash,
  faWarning,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { Column } from "primereact/column";
import { DataTable } from "primereact/datatable";
import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import ProgressBar, {
  IProgressMarker,
} from "views/components/ProgressBar/ProgressBar";

import {
  IPortfolio,
  IPortfolioMetadata,
  IPortfolios,
  DEFAULT_PORTFOLIO_ID,
} from "views/definitions/ProgramReviewTool.types";

import { formatSeconds } from "views/utils/FormatUtility";

import styles from "views/containers/PortfolioMenu/PortfolioMenu.module.css";

/** Properties for the PortfolioMenu component. */
interface IPortfolioMenuProps {
  /** Available portfolios. */
  portfolios: IPortfolios;

  /** The currently selected portfolio. */
  selectedPortfolio?: IPortfolio;

  /** Loading state of menu. */
  loading?: boolean;

  /** Current progress marker of portfolio generation status. */
  currentMarker?: number | null;

  /** Progress markers with status of portfolio generation. */
  progressMarkers?: IProgressMarker[];

  /** Callback to invoke when a portfolio should be deleted.
   * @param key The id of the portfolio.
   */
  deletePortfolio: (key: number) => void;

  /** Callback to invoke when the portfolio powerpoint should be generated and when polling for status. */
  generatePortfolio: () => void;

  /** Callback to invoke when the portfolio should be saved.
   * @param name The name of the portfolio.
   */
  savePortfolio: (name: string) => void;

  /** Callback to invoke when a portfolio is selected.
   * @param key The id of the portfolio.
   */
  setPortfolio: (key: number | null) => void;
}

export default function PortfolioMenu({
  portfolios,
  selectedPortfolio,
  loading,
  currentMarker,
  progressMarkers,
  deletePortfolio,
  generatePortfolio,
  savePortfolio,
  setPortfolio,
}: IPortfolioMenuProps) {
  const [showSaveModal, setShowSaveModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);
  const [showUnsavedModal, setShowUnsavedModal] = React.useState(false);

  const [isLoading, setIsLoading] = React.useState(false);

  const [deletePortfolioID, setDeletePortfolioId] = React.useState<
    number | null
  >(null);
  const [deletePortfolioName, setDeletePortfolioName] = React.useState<
    string | null
  >(null);

  const [selectedPortfolioName, setSelectedPortfolioName] = React.useState(
    selectedPortfolio?.name
  );

  const [newSelectionId, setNewSelectionId] = React.useState<number | null>(
    null
  );

  React.useEffect(() => {
    setSelectedPortfolioName(selectedPortfolio?.name);
  }, [selectedPortfolio]);

  /* Added to prevent stuttering on inital render. */
  React.useEffect(() => {
    setIsLoading(loading ?? true);
  }, [loading]);

  const handleSavePortfolio = React.useCallback(() => {
    if (!selectedPortfolioName?.length) {
      toast.error("Error: Cannot save without a portfolio name.");
      return;
    }

    if (
      Object.values(portfolios ?? {}).some(
        (portfolio) =>
          portfolio.name.toLowerCase() ===
            selectedPortfolioName.toLowerCase() &&
          selectedPortfolio?.id !== portfolio.id
      )
    ) {
      toast.error("Error: Duplicate portfolio name.");
      return;
    }

    savePortfolio(selectedPortfolioName);
    setShowSaveModal(false);
  }, [portfolios, selectedPortfolio, selectedPortfolioName, savePortfolio]);

  const handleCancelPortfolio = React.useCallback(() => {
    setSelectedPortfolioName(selectedPortfolio?.name);
    setShowSaveModal(false);
  }, [selectedPortfolio]);

  const handleDeletePortfolio = React.useCallback(() => {
    if (deletePortfolioID) {
      deletePortfolio(deletePortfolioID);
    }
    setShowDeleteModal(false);
  }, [deletePortfolioID, deletePortfolio]);

  // Checks for unsaved portfolio data before either making the new selection or confirming the new selection.
  const handleSetPortfolio = React.useCallback(
    (newSelection?: number) => {
      // Select portfolio if no portfolio is currently selected.
      if (!selectedPortfolio) {
        setPortfolio(newSelection ?? null);
        return;
      }

      const currentPrograms = Object.keys(selectedPortfolio?.programs ?? {});
      const storedPrograms = Object.keys(
        (portfolios ?? {})[selectedPortfolio?.id]?.programs || {}
      );

      // Confirm when portfolio's current programs do not match stored portfolio programs.
      if (
        currentPrograms.length !== storedPrograms.length ||
        !storedPrograms.every((program) => currentPrograms.includes(program))
      ) {
        setNewSelectionId(newSelection ?? null);
        setShowUnsavedModal(true);
        return;
      }

      // Select portfolio.
      setPortfolio(newSelection ?? null);
    },
    [portfolios, selectedPortfolio, setPortfolio]
  );

  const deleteButtonTemplate = React.useCallback(
    (rowData: IPortfolioMetadata) => {
      return (
        <button
          className={styles["delete-portfolio-button"]}
          onClick={(event) => {
            event.stopPropagation();
            setShowDeleteModal(true);
            setDeletePortfolioId(rowData.id);
            setDeletePortfolioName(rowData.name);
          }}
          aria-label="delete portfolio"
        >
          <FontAwesomeIcon
            className={styles["portfolio-menu-icon"]}
            icon={faTrash}
          />
        </button>
      );
    },
    []
  );

  const formatDateTemplate = React.useCallback(
    (rowData: IPortfolioMetadata) => {
      return (
        <>
          <span
            className={styles["date-long"]}
            aria-description="long date format"
          >
            {new Date(rowData.modified).toLocaleString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </span>
          <span
            className={styles["date-short"]}
            aria-description="short date format"
          >
            {new Date(rowData.modified).toLocaleString("en-US", {
              year: "numeric",
              month: "numeric",
              day: "numeric",
            })}
          </span>
        </>
      );
    },
    []
  );

  const reducedPortfolios = React.useCallback((portfolios: IPortfolios) => {
    return portfolios
      ? (Object.values(portfolios).map((portfolio) => ({
          id: portfolio.id,
          name: portfolio.name,
          modified: portfolio.modified,
          numberOfPrograms: portfolio.programs
            ? Object.keys(portfolio.programs).length
            : 0,
        })) as IPortfolioMetadata[])
      : [];
  }, []);

  return (
    <div
      className={styles["portfolio-menu"]}
      aria-description="container for portfolio table and controls "
    >
      {progressMarkers?.length ? (
        <ProgressBar
          className={styles["portfolio-progress-bar"]}
          progressMarkers={progressMarkers}
          currentMarker={currentMarker}
          showValue={true}
          striped={true}
          discreteUnit={""}
        />
      ) : (
        <>
          <button
            disabled={
              !Object.values(selectedPortfolio?.programs ?? {}).some(
                (program) => !program.disabled
              )
            }
            onClick={() => generatePortfolio()}
            className={styles["portfolio-menu-button"]}
            aria-label="generate portfolio powerpoint"
            data-tooltip-id="generate-portfolio-tooltip"
            data-tooltip-delay-show={200}
          >
            <span
              className={styles["portfolio-menu-icon"]}
              aria-description="portfolio menu button icon"
            >
              <img
                className={styles["power-point-icon"]}
                src="/thirdParty/power_point.svg"
              ></img>
            </span>
            <span
              className={styles["portfolio-menu-label"]}
              aria-description="portfolio menu button label"
            >
              Generate Slides
            </span>
          </button>
          <Tooltip id="generate-portfolio-tooltip" place={"left"}>
            Program Review will be cached for{" "}
            {formatSeconds(__PROGRAM_REVIEW_EXPORT_CACHE_TIMEOUT_SECONDS__)}
          </Tooltip>
        </>
      )}

      <button
        disabled={Object.keys(selectedPortfolio?.programs ?? {}).length < 1}
        onClick={() => setShowSaveModal(true)}
        className={styles["portfolio-menu-button"]}
        aria-label="save portfolio"
      >
        <FontAwesomeIcon
          icon={faSave}
          className={styles["portfolio-menu-icon"]}
        />
        <span
          className={styles["portfolio-menu-label"]}
          aria-description="portfolio menu button label"
        >
          Save Portfolio
        </span>
      </button>

      <button
        onClick={() => handleSetPortfolio()}
        className={styles["portfolio-menu-button"]}
        aria-label="create new portfolio"
      >
        <FontAwesomeIcon
          icon={faPlusSquare}
          className={styles["portfolio-menu-icon"]}
        />
        <span
          className={styles["portfolio-menu-label"]}
          aria-description="portfolio menu button label"
        >
          New Portfolio
        </span>
      </button>
      <DataTable
        className={styles["portfolio-table"]}
        value={reducedPortfolios(portfolios)}
        emptyMessage={!loading ? "No Portfolios found." : " "}
        dataKey="id"
        loading={isLoading}
        loadingIcon={<MoonLoader />}
        scrollable
        scrollHeight="flex"
        selectionMode="single"
        selection={reducedPortfolios(portfolios).find(
          (portfolio) => portfolio.id === selectedPortfolio?.id
        )}
        onSelectionChange={(event) => {
          if (event.value) {
            handleSetPortfolio(event.value.id);
          }
        }}
        sortField="modified"
        sortOrder={-1}
      >
        <Column
          sortable
          field="name"
          header="Name"
          bodyClassName={styles["standard-td"]}
        ></Column>
        <Column
          sortable
          field="modified"
          body={formatDateTemplate}
          header="Modified"
          bodyClassName={styles["standard-td"]}
        ></Column>
        <Column
          body={deleteButtonTemplate}
          bodyClassName={styles["button-td"]}
        />
      </DataTable>
      <ConfirmModal
        title={
          selectedPortfolio?.id === DEFAULT_PORTFOLIO_ID
            ? "Save New Portfolio"
            : "Save Changes"
        }
        open={showSaveModal}
        acceptLabel={<>Save</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleSavePortfolio()}
        acceptClassName={styles["confirm-save-button"]}
        onReject={() => handleCancelPortfolio()}
      >
        <label>
          Portfolio Name:
          <input
            value={selectedPortfolioName}
            onChange={(event) => setSelectedPortfolioName(event.target.value)}
            className={styles["portfolio-name-input"]}
            type="text"
            aria-description="input for portfolio name"
            placeholder="Portfolio Name"
          />
        </label>
        {selectedPortfolio?.id !== DEFAULT_PORTFOLIO_ID && (
          <p
            className={styles["overwrite-warning"]}
            aria-description="overwrite warning description"
          >
            <FontAwesomeIcon
              className={styles["portfolio-menu-icon"]}
              icon={faWarning}
            />
            This will overwrite an existing portfolio
          </p>
        )}
      </ConfirmModal>
      <ConfirmModal
        title={"Delete Portfolio"}
        open={showDeleteModal}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleDeletePortfolio()}
        acceptClassName={styles["confirm-delete-button"]}
        onReject={() => setShowDeleteModal(false)}
      >
        <p aria-description="delete warning description">
          Portfolio to be deleted: <b>{deletePortfolioName}</b>
        </p>
      </ConfirmModal>
      <ConfirmModal
        title={"Unsaved Changes"}
        open={showUnsavedModal}
        acceptLabel={<>Continue without saving</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => {
          setPortfolio(newSelectionId);
          setShowUnsavedModal(false);
        }}
        acceptClassName={styles["confirm-unsaved-button"]}
        onReject={() => setShowUnsavedModal(false)}
      >
        <p aria-description="unsaved warning description">
          Would you like to continue without saving your current portfolio?
        </p>
      </ConfirmModal>
    </div>
  );
}
