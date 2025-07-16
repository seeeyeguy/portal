import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import { IApiTag } from "state/query/api/portal/directory/TagHelper";
import api from "state/query/api";

import { ITag } from "definitions/portal/directory/Tag.types";

type TApiTagResponse = {
  data: ITag | ITag[] | number;
  status: number | undefined;
};

type TApiSearchTagResponse = { data: ITag[]; status: number | undefined };

export type TApiPostTagRequest = {
  label: string;
};

export type TApiFetchTagRequest = number | null;

export type TApiPutTagRequest = TApiPostTagRequest;

const tagApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addTag: builder.mutation<TApiTagResponse, TApiPostTagRequest>({
      query: (body: TApiPostTagRequest) => ({
        url: endpoints.PORTAL.DIRECTORY.TAGS.BASE(),
        method: POST,
        body,
      }),
      transformResponse: (response: IApiTag, meta): TApiTagResponse => ({
        data: response as ITag,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Tag", "TagSearch"],
    }),
    getTags: builder.query<TApiTagResponse, TApiFetchTagRequest>({
      query: (id: TApiFetchTagRequest = null) =>
        endpoints.PORTAL.DIRECTORY.TAGS.BASE(id),
      transformResponse: (response: IApiTag | IApiTag[], meta) => ({
        data: response as ITag | ITag[],
        status: meta?.response?.status,
      }),
      providesTags: ["Tag"],
    }),
    searchTags: builder.query<TApiSearchTagResponse, string>({
      query: (label: string) => endpoints.PORTAL.DIRECTORY.TAGS.SEARCH(label),
      transformResponse: (response: IApiTag[], meta) => ({
        data: response as ITag[],
        status: meta?.response?.status,
      }),
      providesTags: ["TagSearch"],
    }),
    updateTag: builder.mutation<
      TApiTagResponse,
      { body: TApiPutTagRequest } & { id: number }
    >({
      query: ({ body, id }: { body: TApiPutTagRequest } & { id: number }) => ({
        url: endpoints.PORTAL.DIRECTORY.TAGS.BASE(id),
        method: PUT,
        body,
      }),
      transformResponse: (response: IApiTag, meta): TApiTagResponse => ({
        data: response as ITag,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Tag", "TagSearch"],
    }),
    removeTag: builder.mutation<TApiTagResponse, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.DIRECTORY.TAGS.BASE(id),
        method: DELETE,
      }),
      transformResponse: (response: number, meta): TApiTagResponse => ({
        data: response,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Tag", "TagSearch"],
    }),
  }),
});

export default tagApi;
export const {
  useAddTagMutation,
  useGetTagsQuery,
  useSearchTagsQuery,
  useRemoveTagMutation,
  useUpdateTagMutation,
} = tagApi;
