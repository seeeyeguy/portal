import lodash from "lodash";

import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import { IApiFunction } from "state/query/api/portal/directory/FunctionHelper";
import api from "state/query/api";

import { IFunction } from "definitions/portal/directory/Function.types";

export type TApiFunctionResponse = {
  data: IFunction | IFunction[] | number;
  status: number | undefined;
};

export type TApiPostFunctionRequest = {
  name: string;
  description: string;
};

export type TApiFetchFunctionRequest = number | null;

export type TApiPutFunctionRequest = TApiPostFunctionRequest;

const functionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addFunction: builder.mutation<
      TApiFunctionResponse,
      TApiPostFunctionRequest
    >({
      query: (body: TApiPostFunctionRequest) => ({
        url: endpoints.PORTAL.DIRECTORY.FUNCTIONS(),
        method: POST,
        body,
      }),
      transformResponse: (
        response: IApiFunction,
        meta
      ): TApiFunctionResponse => ({
        data: response as IFunction,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Function"],
    }),
    getFunctions: builder.query<TApiFunctionResponse, TApiFetchFunctionRequest>(
      {
        query: (id: TApiFetchFunctionRequest = null) =>
          endpoints.PORTAL.DIRECTORY.FUNCTIONS(id),
        transformResponse: (response: IApiFunction | IApiFunction[], meta) => ({
          data: response as IFunction | IFunction[],
          status: meta?.response?.status,
        }),
        providesTags: ["Function"],
      }
    ),
    updateFunction: builder.mutation<
      TApiFunctionResponse,
      { body: TApiPutFunctionRequest } & { id: number }
    >({
      query: ({
        body,
        id,
      }: { body: TApiPutFunctionRequest } & { id: number }) => ({
        url: endpoints.PORTAL.DIRECTORY.FUNCTIONS(id),
        method: PUT,
        body,
      }),
      transformResponse: (
        response: IApiFunction,
        meta
      ): TApiFunctionResponse => ({
        data: response as IFunction,
        status: meta?.response?.status,
      }),
      async onQueryStarted({ id, ...patch }, { dispatch, queryFulfilled }) {
        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          functionApi.util.updateQueryData("getFunctions", null, (draft) => {
            const updatedEntries = lodash
              .cloneDeep(draft.data as IFunction[])
              .map((functionEntry) =>
                functionEntry.id === id
                  ? { ...functionEntry, ...patch?.body }
                  : functionEntry
              );
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
          dispatch(api.util.invalidateTags(["Function"]));
        }
      },
    }),
    removeFunction: builder.mutation<TApiFunctionResponse, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.DIRECTORY.FUNCTIONS(id),
        method: DELETE,
      }),
      transformResponse: (response: number, meta): TApiFunctionResponse => ({
        data: response,
        status: meta?.response?.status,
      }),
      async onQueryStarted(id, { dispatch, queryFulfilled }) {
        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          functionApi.util.updateQueryData("getFunctions", null, (draft) => {
            const updatedEntries = lodash
              .cloneDeep(draft.data as IFunction[])
              .filter((functionEntry) => functionEntry.id !== id);
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
          dispatch(api.util.invalidateTags(["Function"]));
        }
      },
    }),
  }),
});

export default functionApi;
export const {
  useAddFunctionMutation,
  useGetFunctionsQuery,
  useRemoveFunctionMutation,
  useUpdateFunctionMutation,
} = functionApi;
