import React from "react";
import { useLoaderData } from "react-router";
import { Dropdown } from "primereact/dropdown";

import FAQModal from "views/components/FAQModal/FAQModal";
import NavBar from "views/components/NavBar/NavBar";
import ProgramPerformanceForm from "views/containers/ProgramPerformanceForm/ProgramPerformanceForm";

import { useGetProfileUserQuery } from "state/query/api/portal/users/UsersApi";

import { IProfile } from "definitions/portal/users/Profile.types";
import { IUser } from "definitions/portal/users/User.types";
import { IRecord } from "views/definitions/ProgramReviewTool.types";
import { reportingPeriods, PATestData } from "./ProgramPerformanceProps";

import styles from "views/pages/ProgramPerformance/ProgramPerformance.module.css";

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

  const [selectedPA, setSelectedPA] = React.useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = React.useState(
    reportingPeriods[0]
  );

  const record: IRecord | null = React.useMemo(() => {
    if (!selectedPA || !selectedPeriod) return null;
    const data = PATestData[selectedPA] || null;
    return data.find((d) => d.reportingPeriod === selectedPeriod) || null;
  }, [selectedPA, selectedPeriod]);

  if (!loaderData.user.email) {
    return <div>:x: 404</div>;
  }

  return (
    <>
      <FAQModal />

      <NavBar hideSearchBar profile={profile} />
      <div id="page-content">
        <div
          className={styles["program-performance-inputs"]}
          aria-description="container for program performance inputs"
        >
          <div
            className={styles["program-performance-inputs-background"]}
            aria-description="container for the background of the program performance inputs"
          />

          <h1 aria-description="program performance title">
            Program Performance
          </h1>

          <div className={styles["filter-buttons-row"]}>
            <header>
              <h2>Reporting Period:</h2>
            </header>
            <Dropdown
              value={selectedPeriod}
              onChange={(event) => setSelectedPeriod(event.value)}
              options={reportingPeriods.map((period) => ({
                label: period,
                value: period,
              }))}
              placeholder="Select a Period"
              className={styles["dropdowns"]}
            />
            <header>
              <h2>Select Project ID (PA):</h2>
            </header>
            <Dropdown
              value={selectedPA}
              onChange={(event) => setSelectedPA(event.value)}
              options={Object.keys(PATestData).map((PA) => ({
                label: PA,
                value: PA,
              }))}
              placeholder="Select a PA"
              className={styles["dropdowns"]}
            />
          </div>
        </div>

        <ProgramPerformanceForm
          isEditable={
            reportingPeriods.findIndex(
              (period) => period === selectedPeriod
            ) === 0
          }
          selectedPA={selectedPA ?? ""}
          record={record}
        />
      </div>
    </>
  );
}
