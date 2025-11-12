import React from "react";
import { useLoaderData } from "react-router";
import { MoonLoader } from "react-spinners";
import { Dropdown } from "primereact/dropdown";

import FAQModal from "views/components/FAQModal/FAQModal";
import { FAQ_CONTEXTS } from "views/components/FAQModal/FAQModalProps";
import NavBar from "views/components/NavBar/NavBar";
import ProgramPerformanceForm from "views/containers/ProgramPerformanceForm/ProgramPerformanceForm";

import { useGetProgramsQuery } from "state/query/api/portal/programReviewTool/ProgramApi";
import {
  useGetRecordQuery,
  useGetReportingPeriodQuery,
} from "state/query/api/portal/programReviewTool/RecordApi";
import { useGetProfileUserQuery } from "state/query/api/portal/users/UsersApi";

import { IProfile } from "definitions/portal/users/Profile.types";
import { IUser } from "definitions/portal/users/User.types";

import styles from "views/pages/ProgramPerformance/ProgramPerformance.module.css";

const SCROLL_HEIGHT = 87;

export default function ProgramPerformance() {
  const loaderData = useLoaderData() as { user: IUser };

  const { data: profileApiResponse } = useGetProfileUserQuery(
    loaderData.user.email
  );
  const profile = (profileApiResponse?.data ?? {
    user: {
      firstName: loaderData.user.firstName,
      lastName: loaderData.user.lastName,
      email: loaderData.user.email,
    },
    jobTitle: "UNKNOWN",
    citizenship: "UNKNOWN",
  }) as IProfile;

  const { data: programs, isLoading: isLoadingPrograms } = useGetProgramsQuery({
    programMember: loaderData.user.email,
    tiers: [1, 2],
  });

  const { data: reportingPeriods, isLoading: isLoadingReportingPeriods } =
    useGetReportingPeriodQuery(1);

  const [edit, setEdit] = React.useState(false);
  const toggleEdit = () => setEdit((prev) => !prev);

  const [selectedPA, setSelectedPA] = React.useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = React.useState<number>();

  // Adds class to menu when scrolled past a certain point.
  const pageContentRef = React.useRef<HTMLDivElement>(null);
  const [scrolled, setScrolled] = React.useState(false);

  React.useEffect(() => {
    const container = pageContentRef.current;
    if (!container) return;

    const onScroll = () => {
      setScrolled(container.scrollTop > SCROLL_HEIGHT);
    };

    container.addEventListener("scroll", onScroll);
    return () => container.removeEventListener("scroll", onScroll);
  }, []);

  // Once reporting periods load in, set the initial dropdown value to the first period.
  React.useEffect(() => {
    if (reportingPeriods) {
      setSelectedPeriod(reportingPeriods[0]);
    }
  }, [reportingPeriods]);

  const inCurrentPeriod = React.useMemo(
    () =>
      reportingPeriods?.findIndex((period) => period === selectedPeriod) === 0,
    [reportingPeriods, selectedPeriod]
  );

  const { data: record, isFetching: isFetchingRecord } = useGetRecordQuery({
    paNumber: selectedPA ?? "",
    reportingPeriod: selectedPeriod as number,
    refresh: edit,
  });

  // If reporting period or PA is changed, reset editing state.
  React.useEffect(() => {
    setEdit(false);
  }, [selectedPeriod, selectedPA]);

  const handleEdit = React.useCallback(
    (value: boolean) => setEdit(value),
    [setEdit]
  );

  const periodOptions = React.useMemo(
    () =>
      reportingPeriods?.map((period) => ({
        label: period,
        value: period,
      })) ?? [],
    [reportingPeriods]
  );

  const handlePeriodChange = React.useCallback((event: { value: number }) => {
    setSelectedPeriod(event.value);
  }, []);

  const programOptions = React.useMemo(
    () =>
      Object.keys(programs?.data ?? []).map((PA) => ({
        label: PA,
        value: PA,
      })),
    [programs?.data]
  );

  const handlePAChange = React.useCallback(
    (event: { value: string | null }) => {
      setSelectedPA(event.value);
    },
    []
  );

  if (!loaderData.user.email) {
    return <div>:x: 404</div>;
  }

  return (
    <>
      <FAQModal context={FAQ_CONTEXTS.PPR} />
      <NavBar hideSearchBar profile={profile} />
      <div id="page-content" ref={pageContentRef}>
        <span className={styles["menu-break-top"]} />
        <header className={styles["program-performance"]}>
          <div
            className={styles["program-performance-background"]}
            aria-description="container for the background of the program performance inputs"
          />

          <h1 aria-description="page title">Program Performance</h1>

          {!isLoadingPrograms && !isLoadingReportingPeriods && (
            <div
              className={`${styles["record-controls"]} ${scrolled ? styles["record-scrolled"] : ""}`}
              aria-description="container for selecting program performance record"
            >
              <span
                className={styles["record-select"]}
                aria-description="container for selecting reporting period"
              >
                <header>
                  <h2 className={styles["header-long"]}>Reporting Period:</h2>
                  <h2 className={styles["header-short"]}>Period:</h2>
                </header>
                <Dropdown
                  value={selectedPeriod}
                  onChange={handlePeriodChange}
                  options={periodOptions}
                  placeholder="Reporting Period"
                  className={styles["header-dropdown"]}
                  panelClassName={styles["header-dropdown-panel"]}
                />
              </span>
              <span
                className={styles["record-select"]}
                aria-description="container for selecting pa number"
              >
                <header>
                  <h2 className={styles["header-long"]}>Project ID (PA):</h2>
                  <h2 className={styles["header-short"]}>PA:</h2>
                </header>
                <Dropdown
                  value={selectedPA}
                  onChange={handlePAChange}
                  options={programOptions}
                  placeholder="Select PA"
                  className={styles["header-dropdown"]}
                  panelClassName={styles["header-dropdown-panel"]}
                />
              </span>
              {inCurrentPeriod && (
                <span
                  className={styles["button-container"]}
                  aria-description="container for editing record button"
                >
                  <button
                    type="button"
                    onClick={toggleEdit}
                    className={`${edit ? styles["cancel-button"] : styles["edit-button"]}`}
                    disabled={!record?.data}
                  >
                    {edit ? "Cancel" : "Edit"}
                  </button>
                </span>
              )}
            </div>
          )}
        </header>
        {isLoadingPrograms ||
        isLoadingReportingPeriods ||
        (isFetchingRecord && !edit) ? (
          <div
            className={styles["record-loading"]}
            aria-description="container to display when loading record data"
          >
            <MoonLoader />
          </div>
        ) : !selectedPA && !edit ? (
          <div
            className={styles["awaiting-selection"]}
            aria-description="container to display when awaiting program selection"
          >
            <div className={styles["selection-container"]}>
              <div className={styles["selection-header"]}>
                Select a Reporting Period and Project ID to begin.
              </div>
              <div className={styles["selection-details"]}>
                If you are unable to access your assigned Tier 1 or Tier 2
                programs, please review the Program Team Members in PeopleSoft
                to ensure the program team information is accurate. Additional
                details can be found in the{" "}
                <a href="https://connect.l3harris.com/sites/sas-pgm-mgmt/PRT/_layouts/15/WopiFrame.aspx?sourcedoc=%7bCF03E2D1-964A-40D8-BB09-979297E80AD2%7d&file=PRT%20Web%20FAQ%20and%20Error%20Mitigation.docx&action=default&IsList=1&ListId=%7b8231D670-4D3F-4735-808C-D9ECB08CC79D%7d&ListItemId=84">
                  FAQs
                </a>{" "}
                .
              </div>
            </div>
          </div>
        ) : (
          <ProgramPerformanceForm
            key={`${record?.data.paNumber}-${record?.data.reportingPeriod}`}
            isEditing={inCurrentPeriod && !record?.data.id && edit}
            record={record?.data ?? null}
            handleEdit={handleEdit}
          />
        )}
      </div>
    </>
  );
}
