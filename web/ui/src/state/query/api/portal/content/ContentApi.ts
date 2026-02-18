import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import api from "state/query/api";
import {
  IApiContent,
  transformContentRecord,
} from "state/query/api/portal/content/ContentHelpers";

import { IContent } from "definitions/portal/content/Content.types";

type TApiContentResponse = {
  data: IContent | number;
  status: number | undefined;
};

export type TApiPostContentRequest = {
  key: string;
  content: object;
};

export const MAINTENANCE_BANNERS_CONTENT_KEY = "maintenance_banners";

const transformContentRecordWithKey = (data: IApiContent): IContent => {
  let transformedContent;
  if (data.key === MAINTENANCE_BANNERS_CONTENT_KEY) {
    transformedContent = data.content;
  } else {
    transformedContent = transformContentRecord(data.content);
  }
  return {
    ...transformContentRecord(data),
    content: transformedContent,
  } as IContent;
};

const contentApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addContent: builder.mutation<TApiContentResponse, TApiPostContentRequest>({
      query: (body: TApiPostContentRequest) => ({
        url: endpoints.PORTAL.CONTENT.CONTENT(),
        method: POST,
        body,
      }),
      transformResponse: (
        response: IApiContent,
        meta
      ): TApiContentResponse => ({
        data: transformContentRecordWithKey(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Content"],
    }),
    getContent: builder.query<TApiContentResponse, string>({
      query: (key: string) => ({
        url: endpoints.PORTAL.CONTENT.CONTENT(key),
      }),
      transformResponse: (
        response: IApiContent,
        meta
      ): TApiContentResponse => ({
        data: transformContentRecordWithKey(response),
        status: meta?.response?.status,
      }),
      providesTags: ["Content"],
    }),
    updateContent: builder.mutation<
      TApiContentResponse,
      { body: Omit<TApiPostContentRequest, "key"> } & { key: string }
    >({
      query: ({ body, key }) => ({
        url: endpoints.PORTAL.CONTENT.CONTENT(key),
        method: PUT,
        body,
      }),
      transformResponse: (
        response: IApiContent,
        meta
      ): TApiContentResponse => ({
        data: transformContentRecordWithKey(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Content"],
    }),
    removeContent: builder.mutation<TApiContentResponse, string>({
      query: (key: string) => ({
        url: endpoints.PORTAL.CONTENT.CONTENT(key),
        method: DELETE,
      }),
      transformResponse: (response: number, meta): TApiContentResponse => ({
        data: response,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Content"],
    }),
  }),
});

export default contentApi;
export const {
  useAddContentMutation,
  useGetContentQuery,
  useUpdateContentMutation,
  useRemoveContentMutation,
} = contentApi;
