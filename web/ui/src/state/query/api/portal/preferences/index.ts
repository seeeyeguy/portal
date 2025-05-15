import favoriteApi, {
  useGetFavoritesQuery,
  useAddFavoriteMutation,
  useRemoveFavoriteMutation,
  useOrderFavoritesMutation,
} from "state/query/api/portal/preferences/FavoriteApi";
import queryFilterStateApi, {
  useGetQueryFilterStateQuery,
  usePostQueryFilterStateMutation,
} from "state/query/api/portal/preferences/QueryFilterStateApi";

export default {
  favoriteApi,
  queryFilterStateApi,
  useGetFavoritesQuery,
  useAddFavoriteMutation,
  useRemoveFavoriteMutation,
  useOrderFavoritesMutation,
  useGetQueryFilterStateQuery,
  usePostQueryFilterStateMutation,
};
