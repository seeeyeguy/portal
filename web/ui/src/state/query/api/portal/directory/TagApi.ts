import lodash from "lodash";

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
      invalidatesTags: ["TagSearch"],
      async onQueryStarted({ id, ...patch }, { dispatch, queryFulfilled }) {
        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          tagApi.util.updateQueryData("getTags", null, (draft) => {
            const updatedEntries = lodash
              .cloneDeep(draft.data as ITag[])
              .map((tag) => (tag.id === id ? { ...tag, ...patch?.body } : tag));
            draft.data = updatedEntries;
          })
        );

        try {
          await queryFulfilled;
        } catch {
          /**
           If failure occurs, undo the patch and invalidate the tag
           to perform a re-fetch.
          */
          patchResult.undo();
          dispatch(api.util.invalidateTags(["Tag"]));
        }
      },
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
      invalidatesTags: ["TagSearch"],
      async onQueryStarted(id, { dispatch, queryFulfilled }) {
        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          tagApi.util.updateQueryData("getTags", null, (draft) => {
            const updatedEntries = lodash
              .cloneDeep(draft.data as ITag[])
              .filter((tag) => tag.id !== id);
            draft.data = updatedEntries;
          })
        );

        try {
          await queryFulfilled;
        } catch {
          /**
           If failure occurs, undo the patch and invalidate the tag
           to perform a re-fetch.
          */
          patchResult.undo();
          dispatch(api.util.invalidateTags(["Tag"]));
        }
      },
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
