import endpoints from "services/api";
import { IApiTag } from "state/query/api/portal/directory/TagHelper";
import api from "state/query/api";

import { ITag } from "definitions/portal/directory/Tag.types";

type TApiTagResponse = { data: ITag | ITag[]; status: number | undefined };

type TApiSearchTagResponse = { data: ITag[]; status: number | undefined };

type TApiTagRequest = number | null;

const tagApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getTags: builder.query<TApiTagResponse, TApiTagRequest>({
      query: (id: TApiTagRequest = null) =>
        endpoints.PORTAL.DIRECTORY.TAGS.BASE(id),
      transformResponse: (response: IApiTag | IApiTag[], meta) => ({
        data: response as ITag | ITag[],
        status: meta?.response?.status,
      }),
    }),
    searchTags: builder.query<TApiSearchTagResponse, string>({
      query: (label: string) => endpoints.PORTAL.DIRECTORY.TAGS.SEARCH(label),
      transformResponse: (response: IApiTag[], meta) => ({
        data: response as ITag[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default tagApi;
export const { useGetTagsQuery, useSearchTagsQuery } = tagApi;
