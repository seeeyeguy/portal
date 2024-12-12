import Resource from "state/types/portal/directory/Resource";
import Favorite from "state/types/portal/preferences/Favorite";
import Profile from "state/types/portal/users/Profile";

export interface ResourceLinksProps {
  resources: Resource[];
  favorites: Favorite[];
  profile: Profile;
}
