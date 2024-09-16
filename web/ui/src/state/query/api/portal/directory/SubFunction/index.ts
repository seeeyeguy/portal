import endpoints from "routes/api/endpoints";
import { ApiSubFunction } from "routes/api/helpers/transforms/portal/response/directory/SubFunction";
import api from "state/query/api";
import SubFunction from "state/types/portal/directory/SubFunction";

type ApiSubFunctionResponse = {
  data: SubFunction | SubFunction[];
  status: number | undefined;
};

type ApiSubFunctionRequest = number | null;

const subfunctionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getSubFunctions: builder.query<
      ApiSubFunctionResponse,
      ApiSubFunctionRequest
    >({
      query: (id: ApiSubFunctionRequest = null) =>
        endpoints.PORTAL.DIRECTORY.SUBFUNCTIONS(id),
      transformResponse: (
        response: ApiSubFunction | ApiSubFunction[],
        meta
      ) => ({
        data: response as SubFunction | SubFunction[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default subfunctionApi;
export const { useGetSubFunctionsQuery } = subfunctionApi;
