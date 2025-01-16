import Resource from "state/types/portal/directory/Resource";
import Favorite from "state/types/portal/preferences/Favorite";
import Profile from "state/types/portal/users/Profile";

export interface ResourceLinksProps {
  resources: Resource[];
  favorites: Favorite[];
  profile: Profile;
}

export type ResourceFavoriteMap = {
  [key: string]: { id: string; favoriteId: number | null };
};
