import endpoints from "services/api";
import { DELETE, POST, PUT } from "definitions/RequestConstants";
import transformFavoriteRecord, {
  IApiFavorite,
} from "state/query/api/portal/preferences/FavoriteHelper";
import api from "state/query/api";

import { IFavorite } from "definitions/portal/preferences/Favorite.types";

type TApiFavoriteResponse = {
  data: IFavorite | IFavorite[] | number;
  status: number | undefined;
};

export type TApiFavoriteRequest = { resource: number };

export type TApiFavoriteOrderRequest = { id: number; rank: number }[];

const favoriteApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addFavorite: builder.mutation<TApiFavoriteResponse, TApiFavoriteRequest>({
      query: (body: TApiFavoriteRequest) => ({
        url: endpoints.PORTAL.PREFERENCES.FAVORITES(),
        method: POST,
        body,
      }),
      transformResponse: (response: IApiFavorite, meta) => ({
        data: transformFavoriteRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Favorite"],
    }),
    removeFavorite: builder.mutation<TApiFavoriteResponse, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.PREFERENCES.FAVORITES(id),
        method: DELETE,
      }),
      transformResponse: (response: number, meta) => ({
        data: response,
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Favorite"],
    }),
    getFavorites: builder.query<TApiFavoriteResponse, string>({
      query: (user: string) => endpoints.PORTAL.PREFERENCES.FAVORITES(user),
      transformResponse: (response: IApiFavorite[], meta) => ({
        data: response.map((favorite) => transformFavoriteRecord(favorite)),
        status: meta?.response?.status,
      }),
      providesTags: ["Favorite"],
    }),
    orderFavorites: builder.mutation<
      TApiFavoriteResponse,
      TApiFavoriteOrderRequest
    >({
      query: (body: TApiFavoriteOrderRequest) => ({
        url: endpoints.PORTAL.PREFERENCES.FAVORITES(),
        method: PUT,
        body: body,
      }),
      transformResponse: (response: IApiFavorite[], meta) => ({
        data: response.map((favorite) => transformFavoriteRecord(favorite)),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Favorite"],
    }),
  }),
});

export default favoriteApi;
export const {
  useGetFavoritesQuery,
  useAddFavoriteMutation,
  useRemoveFavoriteMutation,
  useOrderFavoritesMutation,
} = favoriteApi;
