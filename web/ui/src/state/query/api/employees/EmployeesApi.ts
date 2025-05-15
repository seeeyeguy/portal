import endpoints from "services/api";
import { POST } from "definitions/RequestConstants";
import api from "state/query/api";

import * as types from "definitions/Ldap.types";

type TEmployeesApiResponse = {
  data: types.TEmployee[];
  status: number | undefined;
};

type TEmployeesApiRequest = {
  searchTerm: string;
  offset: number;
  limit: number;
};

const employeesApi = api.injectEndpoints({
  endpoints: (builder) => ({
    searchEmployees: builder.query<TEmployeesApiResponse, TEmployeesApiRequest>(
      {
        query: ({ searchTerm, offset, limit }: TEmployeesApiRequest) => ({
          url: endpoints.SERVICE.LDAP.SEARCH,
          method: POST,
          body: {
            search_term: searchTerm,
            offset,
            limit,
          },
        }),
        transformResponse: (
          response: types.TEmployeeSearchResponse,
          meta
        ): TEmployeesApiResponse => ({
          data: response.entries,
          status: meta?.response?.status,
        }),
      }
    ),
  }),
});

export default employeesApi;
export const { useSearchEmployeesQuery } = employeesApi;
