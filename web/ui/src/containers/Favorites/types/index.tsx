import Favorite from "state/types/portal/preferences/Favorite";
import Profile from "state/types/portal/users/Profile";

export interface FavoritesProps {
  favorites: Favorite[];
  profile: Profile;
}
