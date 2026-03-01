import { useLoaderData } from "react-router";

import FilterButtons from "views/components/FilterButtons/FilterButtons";

import {
  toggleEmployeeLevel,
  toggleFunction,
} from "state/actions/ResourceSearchActions";
import { useGetEmployeeLevelsQuery } from "state/query/api/portal/directory/EmployeeLevelApi";
import { useGetFunctionsQuery } from "state/query/api/portal/directory/FunctionApi";
import { useGetQueryFilterStateQuery } from "state/query/api/portal/preferences/QueryFilterStateApi";
import { useTypedSelector } from "state/store/store";

import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";
import { IFunction } from "definitions/portal/directory/Function.types";
import { IAuthUser } from "definitions/Sso.types";

import styles from "views/containers/Controls/Controls.module.css";

export default function Controls() {
  const { employeeLevels: employeeLevelIds, functions: functionIds } =
    useTypedSelector((state) => state.ResourceSearch);

  const rtkEmployeeLevelsQuery = useGetEmployeeLevelsQuery(null);
  const rtkFunctionsQuery = useGetFunctionsQuery(null);

  const employeeLevels = (rtkEmployeeLevelsQuery.data?.data ??
    []) as IEmployeeLevel[];
  const functions = (rtkFunctionsQuery.data?.data ?? []) as IFunction[];

  const loaderData = useLoaderData() as { user: IAuthUser };

  const { data: queryFilterStateApiResponse } = useGetQueryFilterStateQuery(
    loaderData.user.username
  );
  const queryFilterStateId = queryFilterStateApiResponse?.data.id;

  return (
    <>
      <div
        className={styles["role-buttons"]}
        aria-description="container for role filter buttons"
      >
        <div
          className={styles["role-buttons-background"]}
          aria-description="container for the background of the role filter buttons"
        />
        <h1 aria-description="segment of company">
          Space and Mission Systems
        </h1>

        <FilterButtons
          title="Role"
          records={employeeLevels}
          activeFilters={employeeLevelIds}
          toggleAction={toggleEmployeeLevel(
            functionIds,
            employeeLevelIds,
            queryFilterStateId
          )}
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
          toggleAction={toggleFunction(
            functionIds,
            employeeLevelIds,
            queryFilterStateId
          )}
        />
      </div>
    </>
  );
}
