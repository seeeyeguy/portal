import endpoints from "services/api";
import { IApiFunction } from "state/query/api/portal/directory/FunctionHelper";
import api from "state/query/api";

import { IFunction } from "definitions/portal/directory/Function.types";

type TApiFunctionResponse = {
  data: IFunction | IFunction[];
  status: number | undefined;
};

type TApiFunctionRequest = number | null;

const functionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getFunctions: builder.query<TApiFunctionResponse, TApiFunctionRequest>({
      query: (id: TApiFunctionRequest = null) =>
        endpoints.PORTAL.DIRECTORY.FUNCTIONS(id),
      transformResponse: (response: IApiFunction | IApiFunction[], meta) => ({
        data: response as IFunction | IFunction[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default functionApi;
export const { useGetFunctionsQuery } = functionApi;
