import React from "react";

import Tag from "state/types/portal/directory/Tag";
import Favorite from "state/types/portal/preferences/Favorite";
import Profile from "state/types/portal/users/Profile";

export interface ResultsProps {
  favorites: Favorite[];
  filterData: React.MutableRefObject<{ [key: string]: string[] }>;
  filterTags: Tag[];
  profile: Profile;
}
