import endpoints from "services/api";
import { POST } from "definitions/RequestConstants";
import {
  transformResourceRecords,
  IApiResource,
  ApiResourceFunctreeResponse,
} from "state/query/api/portal/directory/ResourceHelper";
import api from "state/query/api";

import { TResourceRecords } from "definitions/portal/directory/Resource.types";

type TApiResourceResponse = {
  data: TResourceRecords;
  status: number | undefined;
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
    searchResources: builder.query<
      TApiResourceResponse,
      { body: TApiSearchResourceRequest } & TApiSearchResourceRequestOptional
    >({
      query: ({ body, page = null, limit = null }) => ({
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
export const { useSearchResourcesQuery } = resourceApi;
