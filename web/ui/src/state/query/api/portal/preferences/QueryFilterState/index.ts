import endpoints from "routes/api/endpoints";
import { POST, PUT } from "routes/api/helpers/headers/init";
import transformQueryFilterStateRecord, {
  ApiQueryFilterState,
} from "routes/api/helpers/transforms/portal/response/preferences/QueryFilterState";
import api from "state/query/api";
import QueryFilterState from "state/types/portal/preferences/QueryFilterState";

type ApiQueryFilterStateResponse = {
  data: QueryFilterState;
  status: number | undefined;
};

type ApiQueryFilterStateRequest = string;

type ApiQueryFilterStateMutationRequest = {
  user: string;
  search: number;
  functions: number[];
  employeeLevels: number[];
  tags: number[];
};

const queryFilterStateApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getQueryFilterState: builder.query<
      ApiQueryFilterStateResponse,
      ApiQueryFilterStateRequest
    >({
      query: (user: ApiQueryFilterStateRequest) =>
        endpoints.PORTAL.PREFERENCES.QUERY_FILTER_STATE(user),
      transformResponse: (response: ApiQueryFilterState, meta) => ({
        data: transformQueryFilterStateRecord(response),
        status: meta?.response?.status,
      }),
      providesTags: ["QueryFilterState"],
    }),
    postQueryFilterState: builder.mutation<
      ApiQueryFilterStateResponse,
      { body: ApiQueryFilterStateMutationRequest } & {
        post: boolean;
        id: number | null;
      }
    >({
      query: ({ body, post = true, id = null }) => ({
        url: endpoints.PORTAL.PREFERENCES.QUERY_FILTER_STATE(id),
        method: post ? POST : PUT,
        body: {
          ...body,
          employee_levels: body.employeeLevels,
        },
      }),
      invalidatesTags: ["QueryFilterState"],
    }),
  }),
});

export default queryFilterStateApi;
export const { useGetQueryFilterStateQuery, usePostQueryFilterStateMutation } =
  queryFilterStateApi;
