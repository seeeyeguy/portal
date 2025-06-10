import lodash from "lodash";

import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import api from "state/query/api";
import {
  IApiRequest,
  transformRequestRecord,
} from "state/query/api/portal/request/RequestHelper";

import { IRequest } from "definitions/portal/request/Request.types";

type ValueOf<T> = T[keyof T];

type TApiRequestResponse = {
  data: IRequest | IRequest[] | number;
  status: number | undefined;
};

export type TApiPostRequestRequest = {
  uid: string;
  name: string;
  description: string;
  previousRevision: number | null;
  url: string;
  thumbnail: File | null;
  employeeLevels: number[];
  subfunctions: number[];
  tags: number[];
  pointOfContacts: string[];
  type: string;
  download: boolean;
  stage: "DRAFT" | "SUBMITTED";
};

export type TApiFetchRequestRequest = {
  id?: number | null;
  originator?: string | null;
  stage?: number | null;
  status?: string | null;
  page?: number | null;
  limit?: number | null;
  includeArchived?: boolean | null;
};

export type TApiPutRequestRequest = {
  name: string;
  description: string;
  url: string;
  thumbnail: File;
  employeeLevels: number[];
  subfunctions: number[];
  tags: number[];
  pointOfContacts: string[];
  type: string;
  download: boolean;
  stage: "DRAFT" | "SUBMITTED";
};

const IGNORED_FORM_DATA_VALUES = new Set([undefined, null, ""]);

const requestApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addRequest: builder.mutation<TApiRequestResponse, TApiPostRequestRequest>({
      query: (body: TApiPostRequestRequest) => {
        const formData = new FormData();
        const camelCaseKeys = new Set([
          "previousRevision",
          "employeeLevels",
          "pointOfContacts",
        ]);
        let apiBody: { [k: string]: ValueOf<TApiPostRequestRequest> } =
          Object.entries(body).reduce((acc, [key, value]) => {
            if (!camelCaseKeys.has(key)) {
              return {
                ...acc,
                [key]: value,
              };
            }
            return acc;
          }, {});
        apiBody = {
          ...apiBody,
          previous_revision: body.previousRevision,
          employee_levels: JSON.stringify(body.employeeLevels),
          subfunctions: JSON.stringify(body.subfunctions),
          tags: JSON.stringify(body.tags),
          point_of_contacts: JSON.stringify(body.pointOfContacts),
        };

        for (const key in apiBody) {
          if (!IGNORED_FORM_DATA_VALUES.has(apiBody[key as string])) {
            formData.append(key, apiBody[key as string]);
          }
        }

        return {
          url: endpoints.PORTAL.REQUEST.REQUEST(),
          method: POST,
          body: formData,
          headers: {
            Path: "api/v1/request/request",
          },
        };
      },
      transformResponse: (
        response: IApiRequest,
        meta
      ): TApiRequestResponse => ({
        data: transformRequestRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Request"],
    }),
    getRequests: builder.query<TApiRequestResponse, TApiFetchRequestRequest>({
      query: ({
        id = null,
        originator = null,
        stage = null,
        status = null,
        page = null,
        limit = null,
        includeArchived = null,
      }: TApiFetchRequestRequest) =>
        endpoints.PORTAL.REQUEST.REQUEST(
          id,
          originator,
          stage,
          status,
          page,
          limit,
          includeArchived
        ),
      transformResponse: (
        response: IApiRequest | IApiRequest[],
        meta
      ): TApiRequestResponse => ({
        data: lodash.isArray(response)
          ? response.map((record) => transformRequestRecord(record))
          : transformRequestRecord(response),
        status: meta?.response?.status,
      }),
      providesTags: ["Request"],
    }),
    updateRequest: builder.mutation<
      TApiRequestResponse,
      { body: TApiPutRequestRequest } & { id: number }
    >({
      query: ({
        body,
        id,
      }: { body: TApiPutRequestRequest } & { id: number }) => {
        const formData = new FormData();
        const camelCaseKeys = new Set([
          "resourceId",
          "employeeLevels",
          "pointOfContacts",
        ]);
        let apiBody: { [k: string]: ValueOf<TApiPutRequestRequest> } =
          Object.entries(body).reduce((acc, [key, value]) => {
            if (!camelCaseKeys.has(key)) {
              return {
                ...acc,
                [key]: value,
              };
            }
            return acc;
          }, {});
        apiBody = {
          ...apiBody,
          employee_levels: JSON.stringify(body.employeeLevels),
          subfunctions: JSON.stringify(body.subfunctions),
          tags: JSON.stringify(body.tags),
          point_of_contacts: JSON.stringify(body.pointOfContacts),
        };

        for (const key in apiBody) {
          if (!IGNORED_FORM_DATA_VALUES.has(apiBody[key as string])) {
            formData.append(key, apiBody[key as string]);
          }
        }

        return {
          url: endpoints.PORTAL.REQUEST.REQUEST(id),
          method: PUT,
          body: formData,
          headers: {
            Path: "api/v1/request/request",
          },
        };
      },
      transformResponse: (
        response: IApiRequest,
        meta
      ): TApiRequestResponse => ({
        data: transformRequestRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Request"],
    }),
    removeRequest: builder.mutation<TApiRequestResponse, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.REQUEST.REQUEST(id),
        method: DELETE,
      }),
      transformResponse: (response: number, meta): TApiRequestResponse => ({
        data: response,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Request"],
    }),
  }),
});

export default requestApi;
export const {
  useAddRequestMutation,
  useGetRequestsQuery,
  useRemoveRequestMutation,
  useUpdateRequestMutation,
} = requestApi;
