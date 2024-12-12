import endpoints from "routes/api/endpoints";
import { ApiFunction } from "routes/api/helpers/transforms/portal/response/directory/Function";
import api from "state/query/api";

import PortalFunction from "state/types/portal/directory/Function";

type ApiFunctionResponse = {
  data: PortalFunction | PortalFunction[];
  status: number | undefined;
};

type ApiFunctionRequest = number | null;

const functionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getFunctions: builder.query<ApiFunctionResponse, ApiFunctionRequest>({
      query: (id: ApiFunctionRequest = null) =>
        endpoints.PORTAL.DIRECTORY.FUNCTIONS(id),
      transformResponse: (response: ApiFunction | ApiFunction[], meta) => ({
        data: response as PortalFunction | PortalFunction[],
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default functionApi;
export const { useGetFunctionsQuery } = functionApi;
