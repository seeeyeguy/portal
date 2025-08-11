import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import { IApiSubFunction } from "state/query/api/portal/directory/SubFunctionHelper";

import api from "state/query/api";

import { ISubFunction } from "definitions/portal/directory/SubFunction.types";

type TApiSubFunctionResponse = {
  data: ISubFunction | ISubFunction[] | number;
  status: number | undefined;
};

export type TApiPostSubFunctionRequest = {
  name: string;
  description: string;
  function: number;
};

export type TApiFetchSubFunctionRequest = number | null;

export type TApiPutSubFunctionRequest = TApiPostSubFunctionRequest;

const subfunctionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addSubFunction: builder.mutation<
      TApiSubFunctionResponse,
      TApiPostSubFunctionRequest
    >({
      query: (body: TApiPostSubFunctionRequest) => ({
        url: endpoints.PORTAL.DIRECTORY.SUBFUNCTIONS(),
        method: POST,
        body,
      }),
      transformResponse: (
        response: IApiSubFunction,
        meta
      ): TApiSubFunctionResponse => ({
        data: response as ISubFunction,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["SubFunction"],
    }),
    getSubFunctions: builder.query<
      TApiSubFunctionResponse,
      TApiFetchSubFunctionRequest
    >({
      query: (id: TApiFetchSubFunctionRequest = null) => ({
        url: endpoints.PORTAL.DIRECTORY.SUBFUNCTIONS(id),
        headers: { "Cache-Control": "max-age=0" },
      }),
      transformResponse: (
        response: IApiSubFunction | IApiSubFunction[],
        meta
      ): TApiSubFunctionResponse => ({
        data: response as ISubFunction | ISubFunction[],
        status: meta?.response?.status,
      }),
      providesTags: ["SubFunction"],
    }),
    updateSubFunction: builder.mutation<
      TApiSubFunctionResponse,
      { body: TApiPutSubFunctionRequest } & { id: number }
    >({
      query: ({
        body,
        id,
      }: { body: TApiPutSubFunctionRequest } & { id: number }) => ({
        url: endpoints.PORTAL.DIRECTORY.SUBFUNCTIONS(id),
        method: PUT,
        body,
      }),
      transformResponse: (
        response: IApiSubFunction,
        meta
      ): TApiSubFunctionResponse => ({
        data: response as ISubFunction,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["SubFunction"],
    }),
    removeSubFunction: builder.mutation<TApiSubFunctionResponse, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.DIRECTORY.SUBFUNCTIONS(id),
        method: DELETE,
      }),
      transformResponse: (response: number, meta): TApiSubFunctionResponse => ({
        data: response,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["SubFunction"],
    }),
  }),
});

export default subfunctionApi;
export const {
  useAddSubFunctionMutation,
  useGetSubFunctionsQuery,
  useRemoveSubFunctionMutation,
  useUpdateSubFunctionMutation,
} = subfunctionApi;
