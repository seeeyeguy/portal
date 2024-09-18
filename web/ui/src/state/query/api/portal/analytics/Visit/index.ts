import endpoints from "routes/api/endpoints";
import { POST } from "routes/api/helpers/headers/init";
import transformVisitRecord, {
  ApiVisit,
} from "routes/api/helpers/transforms/portal/response/analytics/Visit";
import api from "state/query/api";
import Visit from "state/types/portal/analytics/Visit";

type ApiVisitResponse = { data: Visit; status: number | undefined };

type ApiVisitRequest = { user: string; resource: number };

const visitApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addVisit: builder.mutation<ApiVisitResponse, ApiVisitRequest>({
      query: (body: ApiVisitRequest) => ({
        url: endpoints.PORTAL.ANALYTICS.VISITS,
        method: POST,
        body,
      }),
      transformResponse: (response: ApiVisit, meta): ApiVisitResponse => ({
        data: transformVisitRecord(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default visitApi;
export const { useAddVisitMutation } = visitApi;
