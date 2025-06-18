import endpoints from "services/api";
import { POST, PUT } from "definitions/RequestConstants";
import transformQueryFilterStateRecord, {
  ApiQueryFilterState,
} from "state/query/api/portal/preferences/QueryFilterStateHelper";
import api from "state/query/api";

import { IQueryFilterState } from "definitions/portal/preferences/QueryFilterState.types";

type TApiQueryFilterStateResponse = {
  data: IQueryFilterState;
  status: number | undefined;
};

type TApiQueryFilterStateRequest = string;

export type TApiQueryFilterStateMutationRequest = {
  search: number | null;
  functions: number[];
  employeeLevels: number[];
  tags: number[];
};

const queryFilterStateApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getQueryFilterState: builder.query<
      TApiQueryFilterStateResponse,
      TApiQueryFilterStateRequest
    >({
      query: (user: TApiQueryFilterStateRequest) =>
        endpoints.PORTAL.PREFERENCES.QUERY_FILTER_STATE(user),
      transformResponse: (response: ApiQueryFilterState, meta) => ({
        data: transformQueryFilterStateRecord(response),
        status: meta?.response?.status,
      }),
      providesTags: ["QueryFilterState"],
    }),
    postQueryFilterState: builder.mutation<
      TApiQueryFilterStateResponse,
      { body: TApiQueryFilterStateMutationRequest } & {
        post: boolean;
        id: number | null | undefined;
      }
    >({
      query: ({
        body,
        post = true,
        id = null,
      }: { body: TApiQueryFilterStateMutationRequest } & {
        post: boolean;
        id: number | null | undefined;
      }) => ({
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
