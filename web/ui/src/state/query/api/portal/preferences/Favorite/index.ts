import endpoints from "routes/api/endpoints";
import { DELETE, POST, PUT } from "routes/api/helpers/headers/init";
import transformFavoriteRecord, {
  ApiFavorite,
} from "routes/api/helpers/transforms/portal/response/preferences/Favorite";
import api from "state/query/api";
import Favorite from "state/types/portal/preferences/Favorite";

type ApiFavoriteResponse = {
  data: Favorite | Favorite[];
  status: number | undefined;
};

type ApiFavoriteRequest = { user: string; resource: number };

type ApiFavoriteOrderRequest = { id: number; rank: number }[];

const favoriteApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addFavorite: builder.mutation<ApiFavoriteResponse, ApiFavoriteRequest>({
      query: (body: ApiFavoriteRequest) => ({
        url: endpoints.PORTAL.PREFERENCES.FAVORITES(),
        method: POST,
        body,
      }),
      transformResponse: (response: ApiFavorite, meta) => ({
        data: transformFavoriteRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Favorite"],
    }),
    removeFavorite: builder.mutation<ApiFavoriteResponse, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.PREFERENCES.FAVORITES(id),
        method: DELETE,
      }),
      transformResponse: (response: ApiFavorite, meta) => ({
        data: transformFavoriteRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Favorite"],
    }),
    getFavorites: builder.query<ApiFavoriteResponse, string>({
      query: (user: string) => endpoints.PORTAL.PREFERENCES.FAVORITES(user),
      transformResponse: (response: ApiFavorite[], meta) => ({
        data: response.map((favorite) => transformFavoriteRecord(favorite)),
        status: meta?.response?.status,
      }),
      providesTags: ["Favorite"],
    }),
    orderFavorites: builder.mutation<
      ApiFavoriteResponse,
      { body: ApiFavoriteOrderRequest } & { user: string }
    >({
      query: ({ body, user }) => ({
        url: endpoints.PORTAL.PREFERENCES.FAVORITES(user),
        method: PUT,
        body: body,
      }),
      transformResponse: (response: ApiFavorite[], meta) => ({
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
