import endpoints from "services/api";
import {
  IApiProfile,
  transformProfileRecord,
} from "state/query/api/portal/users/UsersHelper";
import api from "state/query/api";

import { IProfile } from "definitions/portal/users/Profile.types";

type TApiProfileResponse = { data: IProfile; status: number | undefined };

const usersApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getProfileUser: builder.query<TApiProfileResponse, string>({
      query: (user: string) => endpoints.PORTAL.USERS.PROFILE(user),
      transformResponse: (
        response: IApiProfile,
        meta
      ): TApiProfileResponse => ({
        data: transformProfileRecord(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default usersApi;
export const { useGetProfileUserQuery } = usersApi;
