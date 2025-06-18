import lodash from "lodash";

import endpoints from "services/api";
import { POST } from "definitions/RequestConstants";
import {
  transformResourceRecord,
  transformResourceRecords,
  IApiResource,
  ApiResourceFunctreeResponse,
} from "state/query/api/portal/directory/ResourceHelper";
import api from "state/query/api";

import {
  IResource,
  TResourceRecords,
} from "definitions/portal/directory/Resource.types";

type TBaseApiResourceResponse = {
  data: IResource | IResource[];
  status: number | undefined;
};

type TSearchApiResourceResponse = {
  data: TResourceRecords;
  status: number | undefined;
};

export type TApiFetchResourceRequest = {
  id?: number | null;
  page?: number | null;
  limit?: number | null;
};

export type TApiSearchResourceRequest = {
  name: string;
  description: string;
  functions: number[];
  subfunctions: number[];
  employeeLevels: number[];
  tags: number[];
  download: boolean | null;
  structure: "default" | "functree";
};

type TApiSearchResourceRequestOptional = {
  page: number | null;
  limit: number | null;
};

const resourceApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getResources: builder.query<
      TBaseApiResourceResponse,
      TApiFetchResourceRequest
    >({
      query: ({
        id = null,
        page = null,
        limit = null,
      }: TApiFetchResourceRequest) =>
        endpoints.PORTAL.DIRECTORY.RESOURCES.BASE(id, page, limit),
      transformResponse: (
        response: IApiResource | IApiResource[],
        meta
      ): TBaseApiResourceResponse => ({
        data: lodash.isArray(response)
          ? response.map((record) => transformResourceRecord(record))
          : transformResourceRecord(response),
        status: meta?.response?.status,
      }),
    }),
    searchResources: builder.query<
      TSearchApiResourceResponse,
      { body: TApiSearchResourceRequest } & TApiSearchResourceRequestOptional
    >({
      query: ({
        body,
        page = null,
        limit = null,
      }: {
        body: TApiSearchResourceRequest;
      } & TApiSearchResourceRequestOptional) => ({
        url: endpoints.PORTAL.DIRECTORY.RESOURCES.SEARCH(page, limit),
        method: POST,
        body: {
          ...body,
          employee_levels: body.employeeLevels,
        },
      }),
      transformResponse: (
        response: ApiResourceFunctreeResponse | IApiResource[],
        meta
      ) => ({
        data: transformResourceRecords(response) as unknown as TResourceRecords,
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default resourceApi;
export const { useGetResourcesQuery, useSearchResourcesQuery } = resourceApi;
