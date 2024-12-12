import type { Filters, Option } from "adas-react-components/types";

import Favorite from "state/types/portal/preferences/Favorite";
import Profile from "state/types/portal/users/Profile";

export interface FilterOptions {
  [key: string]: Option[];
}

export interface ResourcesProps {
  title: string;
  searchTerm: string;
  employeeLevels: number[];
  functions: number[];
  favorites: Favorite[];
  profile: Profile;
  filterOptions: FilterOptions;
  getSelectValues: (id: string) => Option[];
  exportFilters: (id: string) => (filters: Filters) => void;
}
