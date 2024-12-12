import endpoints from "routes/api/endpoints";
import { POST } from "routes/api/helpers/headers/init";
import api from "state/query/api";

import * as types from "state/types/services/ldap";

type EmployeesApiResponse = {
  data: types.Employee[];
  status: number | undefined;
};

type EmployeesApiRequest = {
  searchTerm: string;
  offset: number;
  limit: number;
};

const employeesApi = api.injectEndpoints({
  endpoints: (builder) => ({
    searchEmployees: builder.query<EmployeesApiResponse, EmployeesApiRequest>({
      query: ({ searchTerm, offset, limit }: EmployeesApiRequest) => ({
        url: endpoints.SERVICE.LDAP.SEARCH,
        method: POST,
        body: {
          search_term: searchTerm,
          offset,
          limit,
        },
      }),
      transformResponse: (
        response: types.EmployeeSearchResponse,
        meta
      ): EmployeesApiResponse => ({
        data: response.entries,
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default employeesApi;
export const { useSearchEmployeesQuery } = employeesApi;
