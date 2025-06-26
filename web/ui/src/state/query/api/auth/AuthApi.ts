import { isString } from "lodash";

import endpoints from "services/api/";
import {
  ApiAuthUser,
  transformApiAuthUser,
} from "state/query/api/auth/AuthHelper";
import api from "state/query/api";

import { IAuthUser } from "definitions/Sso.types";

type TAuthApiResponse = {
  data: IAuthUser | string;
  status: number | undefined;
};

const authApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getAuthenticatedUser: builder.query<TAuthApiResponse, void>({
      query: () => endpoints.SERVICE.SSO.USER,
      transformResponse: (
        response: ApiAuthUser | string,
        meta
      ): TAuthApiResponse => ({
        data: isString(response) ? response : transformApiAuthUser(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default authApi;
export const { useGetAuthenticatedUserQuery } = authApi;
