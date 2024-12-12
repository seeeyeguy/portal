import FilterButtons from "components/buttons/FilterButtons";
import NavBar from "components/nav/NavBar";

import { ControlsProps } from "containers/Controls/types";

import {
  toggleEmployeeLevel,
  toggleFunction,
} from "state/actions/portal/directory/Resource/Search";
import { useGetEmployeeLevelsQuery } from "state/query/api/portal/directory/EmployeeLevel";
import { useGetFunctionsQuery } from "state/query/api/portal/directory/Function";
import { useTypedSelector } from "state/store";

import EmployeeLevel from "state/types/portal/directory/EmployeeLevel";
import Function from "state/types/portal/directory/Function";

import styles from "containers/Controls/styles/index.module.css";

export default function Controls({ profile }: ControlsProps) {
  const { employeeLevels: employeeLevelIds, functions: functionIds } =
    useTypedSelector((state) => state.ResourceSearch);

  const rtkEmployeeLevelsQuery = useGetEmployeeLevelsQuery(null);
  const rtkFunctionsQuery = useGetFunctionsQuery(null);

  const employeeLevels = (rtkEmployeeLevelsQuery.data?.data ??
    []) as EmployeeLevel[];
  const functions = (rtkFunctionsQuery.data?.data ?? []) as Function[];

  return (
    <>
      <NavBar profile={profile} />
      <div
        className={styles["role-buttons"]}
        aria-description="container for role filter buttons"
      >
        <FilterButtons
          title="Role"
          records={employeeLevels}
          activeFilters={employeeLevelIds}
          toggleAction={toggleEmployeeLevel}
        />
      </div>
      <div
        className={styles["function-buttons"]}
        aria-description="container for function filter buttons"
      >
        <FilterButtons
          title="Function"
          records={functions}
          activeFilters={functionIds}
          toggleAction={toggleFunction}
        />
      </div>
      <hr />
    </>
  );
}
