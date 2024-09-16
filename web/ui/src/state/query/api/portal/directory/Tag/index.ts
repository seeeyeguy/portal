import endpoints from "routes/api/endpoints";
import { ApiTag } from "routes/api/helpers/transforms/portal/response/directory/Tag";
import api from "state/query/api";
import Tag from "state/types/portal/directory/Tag";

type ApiTagResponse = { data: Tag | Tag[]; status: number | undefined };

type ApiSearchTagResponse = { data: Tag[]; status: number | undefined };

type ApiTagRequest = number | null;

const tagApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getTags: builder.query<ApiTagResponse, ApiTagRequest>({
      query: (id: ApiTagRequest = null) =>
        endpoints.PORTAL.DIRECTORY.TAGS.BASE(id),
      transformResponse: (response: ApiTag | ApiTag[], meta) => ({
        data: response as Tag | Tag[],
        status: meta?.response?.status,
      }),
    }),
    searchTags: builder.query<ApiSearchTagResponse, string>({
      query: (label: string) => endpoints.PORTAL.DIRECTORY.TAGS.SEARCH(label),
      transformResponse: (response: ApiTag[], meta) => ({
        data: response as Tag[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default tagApi;
export const { useGetTagsQuery, useSearchTagsQuery } = tagApi;
