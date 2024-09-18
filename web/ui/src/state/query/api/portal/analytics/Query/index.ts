import endpoints from "routes/api/endpoints";
import { POST } from "routes/api/helpers/headers/init";
import transformQueryRecord, {
  ApiQuery,
} from "routes/api/helpers/transforms/portal/response/analytics/Query";
import api from "state/query/api";
import Query from "state/types/portal/analytics/Query";

type ApiQueryResponse = { data: Query; status: number | undefined };

type ApiQueryRequest = { user: string; searchTerm: number };

const queryApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addQuery: builder.mutation<ApiQueryResponse, ApiQueryRequest>({
      query: (body: ApiQueryRequest) => ({
        url: endpoints.PORTAL.ANALYTICS.QUERIES,
        method: POST,
        body: {
          ...body,
          search_term: body.searchTerm,
        },
      }),
      transformResponse: (response: ApiQuery, meta): ApiQueryResponse => ({
        data: transformQueryRecord(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default queryApi;
export const { useAddQueryMutation } = queryApi;
