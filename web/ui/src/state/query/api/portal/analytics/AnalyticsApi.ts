import endpoints from "services/api";
import { POST } from "definitions/RequestConstants";
import {
  transformQueryRecord,
  IApiQuery,
  transformVisitRecord,
  IApiVisit,
} from "state/query/api/portal/analytics/AnalyticsHelper";
import api from "state/query/api";

import { IQuery, IVisit } from "definitions/portal/Analytics.types";

type TApiQueryResponse = { data: IQuery; status: number | undefined };

export type TApiQueryRequest = { searchTerm: string };

type TApiVisitResponse = { data: IVisit; status: number | undefined };

export type TApiVisitRequest = { resource: number };

const analyticsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addQuery: builder.mutation<TApiQueryResponse, TApiQueryRequest>({
      query: (body: TApiQueryRequest) => ({
        url: endpoints.PORTAL.ANALYTICS.QUERIES,
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
    }),
    addVisit: builder.mutation<TApiVisitResponse, TApiVisitRequest>({
      query: (body: TApiVisitRequest) => ({
        url: endpoints.PORTAL.ANALYTICS.VISITS,
        method: POST,
        body,
      }),
      transformResponse: (response: IApiVisit, meta): TApiVisitResponse => ({
        data: transformVisitRecord(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default analyticsApi;
export const { useAddQueryMutation, useAddVisitMutation } = analyticsApi;
