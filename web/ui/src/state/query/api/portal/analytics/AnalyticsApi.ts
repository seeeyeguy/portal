import lodash from "lodash";

import { POST } from "definitions/RequestConstants";
import endpoints from "services/api";
import {
  transformQueryRecord,
  IApiQuery,
  transformVisitRecord,
  IApiVisit,
} from "state/query/api/portal/analytics/AnalyticsHelper";
import api from "state/query/api";

import { IQuery, IVisit } from "definitions/portal/Analytics.types";

type TApiQueryResponse = {
  data: IQuery | IQuery[];
  status: number | undefined;
};

export type TApiPostQueryRequest = { searchTerm: string };

export type TApiFetchQueryRequest = {
  id?: number | null;
  resourceId?: number | null;
  user?: string | null;
  page?: number | null;
  limit?: number | null;
};

type TApiVisitResponse = {
  data: IVisit | IVisit[];
  status: number | undefined;
};

export type TApiPostVisitRequest = { resource: number };

export type TApiFetchVisitRequest = {
  id?: number | null;
  user?: string | null;
  resource?: number | null;
  page?: number | null;
  limit?: number | null;
};

const analyticsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addQuery: builder.mutation<TApiQueryResponse, TApiPostQueryRequest>({
      query: (body: TApiPostQueryRequest) => ({
        url: endpoints.PORTAL.ANALYTICS.QUERIES(),
        method: POST,
        body: {
          ...body,
          search_term: body.searchTerm,
        },
      }),
      transformResponse: (response: IApiQuery, meta): TApiQueryResponse => ({
        data: transformQueryRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Query"],
    }),
    getQueries: builder.query<TApiQueryResponse, TApiFetchQueryRequest>({
      query: ({
        id = null,
        resourceId = null,
        user = null,
        page = null,
        limit = null,
      }: TApiFetchQueryRequest) =>
        endpoints.PORTAL.ANALYTICS.QUERIES(id, resourceId, user, page, limit),
      transformResponse: (
        response: IApiQuery | IApiQuery[],
        meta
      ): TApiQueryResponse => ({
        data: lodash.isArray(response)
          ? response.map((record) => transformQueryRecord(record))
          : transformQueryRecord(response),
        status: meta?.response?.status,
      }),
      providesTags: ["Query"],
    }),
    addVisit: builder.mutation<TApiVisitResponse, TApiPostVisitRequest>({
      query: (body: TApiPostVisitRequest) => ({
        url: endpoints.PORTAL.ANALYTICS.VISITS(),
        method: POST,
        body,
      }),
      transformResponse: (response: IApiVisit, meta): TApiVisitResponse => ({
        data: transformVisitRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Visit"],
    }),
    getVisits: builder.query<TApiVisitResponse, TApiFetchVisitRequest>({
      query: ({
        id = null,
        user = null,
        resource = null,
        page = null,
        limit = null,
      }: TApiFetchVisitRequest) =>
        endpoints.PORTAL.ANALYTICS.VISITS(id, user, resource, page, limit),
      transformResponse: (
        response: IApiVisit | IApiVisit[],
        meta
      ): TApiVisitResponse => ({
        data: lodash.isArray(response)
          ? response.map((record) => transformVisitRecord(record))
          : transformVisitRecord(response),
        status: meta?.response?.status,
      }),
      providesTags: ["Visit"],
    }),
  }),
});

export default analyticsApi;
export const {
  useAddQueryMutation,
  useGetQueriesQuery,
  useAddVisitMutation,
  useGetVisitsQuery,
} = analyticsApi;
