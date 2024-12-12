import endpoints from "routes/api/endpoints";
import { ApiEmployeeLevel } from "routes/api/helpers/transforms/portal/response/directory/EmployeeLevel";
import api from "state/query/api";

import EmployeeLevel from "state/types/portal/directory/EmployeeLevel";

type ApiEmployeeLevelResponse = {
  data: EmployeeLevel | EmployeeLevel[];
  status: number | undefined;
};

type ApiEmployeeLevelRequest = number | null;

const employeeLevelApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getEmployeeLevels: builder.query<
      ApiEmployeeLevelResponse,
      ApiEmployeeLevelRequest
    >({
      query: (id: ApiEmployeeLevelRequest = null) =>
        endpoints.PORTAL.DIRECTORY.EMPLOYEE_LEVELS(id),
      transformResponse: (
        response: ApiEmployeeLevel | ApiEmployeeLevel[],
        meta
      ): ApiEmployeeLevelResponse => ({
        data: response as EmployeeLevel | EmployeeLevel[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default employeeLevelApi;
export const { useGetEmployeeLevelsQuery } = employeeLevelApi;
