import lodash from "lodash";
import { toast } from "react-toastify";

import { POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import api from "state/query/api";
import {
  IApiAccess,
  transformAccessRecord,
} from "state/query/api/portal/users/AccessHelper";

import { IAccess } from "definitions/portal/users/Access.types";

type TApiAccessResponse = {
  data: IAccess | IAccess[];
  status: number | undefined;
};

export type TApiPostAccessRequest = {
  user: string | null;
  roleLevel: number | null;
  subfunctions: number[];
  stageLevels: number[];
};

export type TApiFetchAccessRequest = {
  id?: number | null;
  user?: string | null;
  roleLevels?: number[] | null;
  subfunctions?: number[] | null;
  includeRevoked?: boolean | null;
};

export type TApiModifyAccessRequest = {
  subfunctions: number[];
};

const accessApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addAccess: builder.mutation<TApiAccessResponse, TApiPostAccessRequest>({
      query: (body: TApiPostAccessRequest) => ({
        url: endpoints.PORTAL.USERS.ACCESS(),
        method: POST,
        body: {
          user: body.user,
          subfunctions: body.subfunctions,
          role_level: body.roleLevel,
          stage_levels: body.stageLevels,
        },
      }),
      transformResponse: (response: IApiAccess, meta): TApiAccessResponse => ({
        data: transformAccessRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Access"],
    }),
    getAccesses: builder.query<TApiAccessResponse, TApiFetchAccessRequest>({
      query: ({
        id = null,
        user = null,
        roleLevels = null,
        subfunctions = null,
        includeRevoked = null,
      }: TApiFetchAccessRequest) =>
        endpoints.PORTAL.USERS.ACCESS(
          id,
          null,
          user,
          roleLevels,
          subfunctions,
          includeRevoked
        ),
      transformResponse: (
        response: IApiAccess | IApiAccess[],
        meta
      ): TApiAccessResponse => ({
        data: lodash.isArray(response)
          ? response.map((record) => transformAccessRecord(record))
          : transformAccessRecord(response),
        status: meta?.response?.status,
      }),
      providesTags: ["Access"],
    }),
    revokeAccess: builder.mutation<TApiAccessResponse, number[]>({
      query: (ids: number[]) => ({
        url: endpoints.PORTAL.USERS.ACCESS(null, ids),
        method: PUT,
      }),
      transformResponse: (response: IApiAccess, meta): TApiAccessResponse => {
        toast.success("Accesses Revoked.");
        return {
          data: transformAccessRecord(response),
          status: meta?.response?.status,
        };
      },
      transformErrorResponse: (response) => {
        toast.error("Accesses Not Revoked.");
        return response;
      },
      invalidatesTags: ["Access"],
    }),
    modifyAccess: builder.mutation<
      TApiAccessResponse,
      { body: TApiModifyAccessRequest } & { id: number }
    >({
      query: ({ id, body }) => ({
        url: endpoints.PORTAL.USERS.ACCESS(
          id,
          null,
          null,
          null,
          null,
          null,
          true
        ),
        method: PUT,
        body,
      }),
      transformResponse: (response: IApiAccess, meta): TApiAccessResponse => ({
        data: transformAccessRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Access"],
    }),
  }),
});

export default accessApi;
export const {
  useAddAccessMutation,
  useGetAccessesQuery,
  useRevokeAccessMutation,
  useModifyAccessMutation,
} = accessApi;
