import { isString } from "lodash";

import endpoints from "services/api/";
import { ApiUser, transformApiUser } from "state/query/api/auth/AuthHelper";
import api from "state/query/api";

import { IUser } from "definitions/Sso.types";

type TAuthApiResponse = { data: IUser | string; status: number | undefined };

const authApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getAuthenticatedUser: builder.query<TAuthApiResponse, void>({
      query: () => endpoints.SERVICE.SSO.USER,
      transformResponse: (
        response: ApiUser | string,
        meta
      ): TAuthApiResponse => ({
        data: isString(response) ? response : transformApiUser(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default authApi;
export const { useGetAuthenticatedUserQuery } = authApi;
