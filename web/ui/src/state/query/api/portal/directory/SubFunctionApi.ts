import lodash from "lodash";

import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import functionApi, {
  TApiFunctionResponse,
} from "state/query/api/portal/directory/FunctionApi";
import { IApiSubFunction } from "state/query/api/portal/directory/SubFunctionHelper";

import api from "state/query/api";

import { IFunction } from "definitions/portal/directory/Function.types";
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
      query: (id: TApiFetchSubFunctionRequest = null) =>
        endpoints.PORTAL.DIRECTORY.SUBFUNCTIONS(id),
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
      async onQueryStarted(
        { id, ...patch },
        { dispatch, queryFulfilled, getState }
      ) {
        /**
          Fetch the IFunction entry from the current
          state since the `patch` has the `Function` id.
        */
        let functionCachedEntries = lodash.cloneDeep(
          (
            getState().api.queries["getFunctions(null)"]
              ?.data as TApiFunctionResponse
          )?.data as IFunction[]
        );

        if (!functionCachedEntries) {
          const response = dispatch(
            functionApi.endpoints.getFunctions.initiate(null)
          );
          const functions = await response;
          functionCachedEntries = (lodash.cloneDeep(functions.data?.data) ??
            []) as IFunction[];
        }

        const functionEntry = functionCachedEntries.find(
          (functionEntry) => functionEntry.id === patch.body.function
        );

        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          subfunctionApi.util.updateQueryData(
            "getSubFunctions",
            null,
            (draft) => {
              const updatedEntries = lodash
                .cloneDeep(draft.data as ISubFunction[])
                .map((subfunction) =>
                  subfunction.id === id
                    ? {
                        ...subfunction,
                        ...patch?.body,
                        function: functionEntry,
                      }
                    : subfunction
                );
              draft.data = updatedEntries as ISubFunction[];
            }
          )
        );

        try {
          await queryFulfilled;
        } catch {
          /**
           If failure occurs, undo the patch and invalidate the tag
           to perform a re-fetch.
          */
          patchResult.undo();
          dispatch(api.util.invalidateTags(["SubFunction"]));
        }
      },
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
      async onQueryStarted(id, { dispatch, queryFulfilled }) {
        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          subfunctionApi.util.updateQueryData(
            "getSubFunctions",
            null,
            (draft) => {
              const updatedEntries = lodash
                .cloneDeep(draft.data as ISubFunction[])
                .filter((subfunction) => subfunction.id !== id);
              draft.data = updatedEntries;
            }
          )
        );

        try {
          await queryFulfilled;
        } catch {
          /**
           If failure occurs, undo the patch and invalidate the tag
           to perform a re-fetch.
          */
          patchResult.undo();
          dispatch(api.util.invalidateTags(["SubFunction"]));
        }
      },
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
