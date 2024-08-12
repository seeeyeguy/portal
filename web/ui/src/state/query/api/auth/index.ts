import { isString } from "lodash";

import endpoints from "routes/api/endpoints";
import {
  ApiUser,
  transformApiUser,
} from "routes/api/helpers/transforms/services/sso";
import api from "state/query/api";
import { User } from "state/types/services/sso";

type AuthApiResponse = { data: User | string; status: number | undefined };

const authApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getAuthenticatedUser: builder.query<AuthApiResponse, void>({
      query: () => endpoints.SERVICE.SSO.USER,
      transformResponse: (
        response: ApiUser | string,
        meta
      ): AuthApiResponse => ({
        data: isString(response) ? response : transformApiUser(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default authApi;
export const { useGetAuthenticatedUserQuery } = authApi;
