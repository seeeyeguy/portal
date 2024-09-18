import favoriteApi, {
  useGetFavoritesQuery,
  useAddFavoriteMutation,
  useRemoveFavoriteMutation,
  useOrderFavoritesMutation,
} from "state/query/api/portal/preferences/Favorite";
import queryFilterStateApi, {
  useGetQueryFilterStateQuery,
  usePostQueryFilterStateMutation,
} from "state/query/api/portal/preferences/QueryFilterState";

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
