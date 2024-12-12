import endpoints from "routes/api/endpoints";
import { POST } from "routes/api/helpers/headers/init";
import {
  transformResourceRecords,
  ApiResource,
  ApiResourceFunctreeResponse,
} from "routes/api/helpers/transforms/portal/response/directory/Resource";
import api from "state/query/api";

import { ResourceRecords } from "state/types/portal/directory/Resource";

type ApiResourceResponse = {
  data: ResourceRecords;
  status: number | undefined;
};

export type ApiSearchResourceRequest = {
  name: string;
  description: string;
  functions: number[];
  subfunctions: number[];
  employeeLevels: number[];
  tags: number[];
  download: boolean | null;
  structure: "default" | "functree";
};

type ApiSearchResourceRequestOptional = {
  page: number | null;
  limit: number | null;
};

const resourceApi = api.injectEndpoints({
  endpoints: (builder) => ({
    searchResources: builder.query<
      ApiResourceResponse,
      { body: ApiSearchResourceRequest } & ApiSearchResourceRequestOptional
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
        response: ApiResourceFunctreeResponse | ApiResource[],
        meta
      ) => ({
        data: transformResourceRecords(response) as unknown as ResourceRecords,
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default resourceApi;
export const { useSearchResourcesQuery } = resourceApi;
