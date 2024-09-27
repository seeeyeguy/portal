import endpoints from "routes/api/endpoints";
import { POST } from "routes/api/helpers/headers/init";
import transformResourceRecord, {
  ApiResource,
} from "routes/api/helpers/transforms/portal/response/directory/Resource";
import api from "state/query/api";
import Resource from "state/types/portal/directory/Resource";

type ApiResourceResponse = { data: Resource[]; status: number | undefined };

type ApiSearchResourceRequest = {
  name: string;
  description: string;
  functions: number[];
  subfunctions: number[];
  employeeLevels: number[];
  tags: number[];
  download: boolean;
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
      transformResponse: (response: ApiResource[], meta) => ({
        data: response.map((resource) => transformResourceRecord(resource)),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default resourceApi;
export const { useSearchResourcesQuery } = resourceApi;
