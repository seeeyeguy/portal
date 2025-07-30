import lodash from "lodash";

import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import { IApiEmployeeLevel } from "state/query/api/portal/directory/EmployeeLevelHelper";
import api from "state/query/api";

import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";

type TApiEmployeeLevelResponse = {
  data: IEmployeeLevel | IEmployeeLevel[] | number;
  status: number | undefined;
};

export type TApiPostEmployeeLevelRequest = {
  name: string;
  description: string;
  level: number;
};

export type TApiFetchEmployeeLevelRequest = number | null;

export type TApiPutEmployeeLevelRequest = {
  name: string;
  description: string;
};

const employeeLevelApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addEmployeeLevel: builder.mutation<
      TApiEmployeeLevelResponse,
      TApiPostEmployeeLevelRequest
    >({
      query: (body: TApiPostEmployeeLevelRequest) => ({
        url: endpoints.PORTAL.DIRECTORY.EMPLOYEE_LEVELS(),
        method: POST,
        body,
      }),
      transformResponse: (
        response: IApiEmployeeLevel,
        meta
      ): TApiEmployeeLevelResponse => ({
        data: response as IEmployeeLevel,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["EmployeeLevel"],
    }),
    getEmployeeLevels: builder.query<
      TApiEmployeeLevelResponse,
      TApiFetchEmployeeLevelRequest
    >({
      query: (id: TApiFetchEmployeeLevelRequest = null) =>
        endpoints.PORTAL.DIRECTORY.EMPLOYEE_LEVELS(id),
      transformResponse: (
        response: IApiEmployeeLevel | IApiEmployeeLevel[],
        meta
      ): TApiEmployeeLevelResponse => ({
        data: response as IEmployeeLevel | IEmployeeLevel[],
        status: meta?.response?.status,
      }),
      providesTags: ["EmployeeLevel"],
    }),
    updateEmployeeLevel: builder.mutation<
      TApiEmployeeLevelResponse,
      { body: TApiPutEmployeeLevelRequest } & { id: number }
    >({
      query: ({
        body,
        id,
      }: { body: TApiPutEmployeeLevelRequest } & { id: number }) => ({
        url: endpoints.PORTAL.DIRECTORY.EMPLOYEE_LEVELS(id),
        method: PUT,
        body,
      }),
      transformResponse: (
        response: IApiEmployeeLevel,
        meta
      ): TApiEmployeeLevelResponse => ({
        data: response as IEmployeeLevel,
        status: meta?.response?.status,
      }),
      async onQueryStarted({ id, ...patch }, { dispatch, queryFulfilled }) {
        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          employeeLevelApi.util.updateQueryData(
            "getEmployeeLevels",
            null,
            (draft) => {
              const updatedEntries = lodash
                .cloneDeep(draft.data as IEmployeeLevel[])
                .map((employeeLevel) =>
                  employeeLevel.id === id
                    ? { ...employeeLevel, ...patch?.body }
                    : employeeLevel
                );
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
          dispatch(api.util.invalidateTags(["EmployeeLevel"]));
        }
      },
    }),
    removeEmployeeLevel: builder.mutation<TApiEmployeeLevelResponse, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.DIRECTORY.EMPLOYEE_LEVELS(id),
        method: DELETE,
      }),
      transformResponse: (response: number, meta) => ({
        data: response,
        status: meta?.response?.status,
      }),
      async onQueryStarted(id, { dispatch, queryFulfilled }) {
        // Perform optimistic update to cache entry.
        const patchResult = dispatch(
          employeeLevelApi.util.updateQueryData(
            "getEmployeeLevels",
            null,
            (draft) => {
              const updatedEntries = lodash
                .cloneDeep(draft.data as IEmployeeLevel[])
                .filter((employeeLevel) => employeeLevel.id !== id);
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
          dispatch(api.util.invalidateTags(["EmployeeLevel"]));
        }
      },
    }),
  }),
});

export default employeeLevelApi;
export const {
  useAddEmployeeLevelMutation,
  useGetEmployeeLevelsQuery,
  useRemoveEmployeeLevelMutation,
  useUpdateEmployeeLevelMutation,
} = employeeLevelApi;
