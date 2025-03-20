import endpoints from "services/api";
import { IApiSubFunction } from "state/query/api/portal/directory/SubFunctionHelper";

import api from "state/query/api";

import { ISubFunction } from "definitions/portal/directory/SubFunction.types";

type TApiSubFunctionResponse = {
  data: ISubFunction | ISubFunction[];
  status: number | undefined;
};

type TApiSubFunctionRequest = number | null;

const subfunctionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getSubFunctions: builder.query<
      TApiSubFunctionResponse,
      TApiSubFunctionRequest
    >({
      query: (id: TApiSubFunctionRequest = null) =>
        endpoints.PORTAL.DIRECTORY.SUBFUNCTIONS(id),
      transformResponse: (
        response: IApiSubFunction | IApiSubFunction[],
        meta
      ) => ({
        data: response as ISubFunction | ISubFunction[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default subfunctionApi;
export const { useGetSubFunctionsQuery } = subfunctionApi;
