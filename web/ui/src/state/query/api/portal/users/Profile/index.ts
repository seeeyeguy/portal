import endpoints from "routes/api/endpoints";
import transformProfileRecord, {
  ApiProfile,
} from "routes/api/helpers/transforms/portal/response/users/Profile";
import api from "state/query/api";
import Profile from "state/types/portal/users/Profile";

type ApiProfileResponse = { data: Profile; status: number | undefined };

const profileApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getProfileUser: builder.query<ApiProfileResponse, string>({
      query: (user: string) => endpoints.PORTAL.USERS.PROFILE(user),
      transformResponse: (response: ApiProfile, meta): ApiProfileResponse => ({
        data: transformProfileRecord(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default profileApi;
export const { useGetProfileUserQuery } = profileApi;
