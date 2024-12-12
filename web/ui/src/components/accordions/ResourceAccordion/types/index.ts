import type {
  Filters,
  Option,
  RecursiveDataSet,
  SelectFilterProps,
} from "adas-react-components/types";

import Resource from "state/types/portal/directory/Resource";
import Favorite from "state/types/portal/preferences/Favorite";
import Profile from "state/types/portal/users/Profile";

export interface RecursiveAccordionChildrenProps {
  childrenId: string;
  dataSet: Resource[];
}

export interface ResourceAccordionProps {
  title: string;
  resources: RecursiveDataSet;
  selectProps: SelectFilterProps[];
  favorites: Favorite[];
  profile: Profile;
  isLoading: boolean;
  getSelectValues: (id: string) => Option[];
  exportFilters: (id: string) => (filters: Filters) => void;
}
