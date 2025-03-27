import endpoints from "services/api";
import { IApiEmployeeLevel } from "state/query/api/portal/directory/EmployeeLevelHelper";
import api from "state/query/api";

import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";

type TApiEmployeeLevelResponse = {
  data: IEmployeeLevel | IEmployeeLevel[];
  status: number | undefined;
};

type TApiEmployeeLevelRequest = number | null;

const employeeLevelApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getEmployeeLevels: builder.query<
      TApiEmployeeLevelResponse,
      TApiEmployeeLevelRequest
    >({
      query: (id: TApiEmployeeLevelRequest = null) =>
        endpoints.PORTAL.DIRECTORY.EMPLOYEE_LEVELS(id),
      transformResponse: (
        response: IApiEmployeeLevel | IApiEmployeeLevel[],
        meta
      ): TApiEmployeeLevelResponse => ({
        data: response as IEmployeeLevel | IEmployeeLevel[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default employeeLevelApi;
export const { useGetEmployeeLevelsQuery } = employeeLevelApi;
