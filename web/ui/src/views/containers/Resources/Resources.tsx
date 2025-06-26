import lodash from "lodash";

import type {
  Filters,
  Option,
  RecursiveDataSet,
} from "adas-react-components/types";

import ResourceAccordion from "views/components/ResourceAccordion/ResourceAccordion";

import { createSelectProps } from "views/utils/ResourcesUtility";

import {
  useSearchResourcesQuery,
  TApiSearchResourceRequest,
} from "state/query/api/portal/directory/ResourceApi";

import { IFilterOptions } from "views/definitions/Resources.types";
import { IResourceFunctree } from "definitions/portal/directory/Resource.types";
import { IFavorite } from "definitions/portal/preferences/Favorite.types";
import { IProfile } from "definitions/portal/users/Profile.types";

export interface IResourcesProps {
  title: string;
  searchTerm: string;
  employeeLevels: number[];
  functions: number[];
  favorites: IFavorite[];
  profile: IProfile;
  filterOptions: IFilterOptions;
  getSelectValues: (id: string) => Option[];
  exportFilters: (id: string) => (filters: Filters) => void;
}

export default function Resources({
  title,
  searchTerm,
  employeeLevels,
  functions,
  favorites,
  profile,
  filterOptions,
  getSelectValues,
  exportFilters,
}: IResourcesProps) {
  const body: TApiSearchResourceRequest = {
    name: searchTerm,
    description: searchTerm,
    functions,
    subfunctions: [],
    employeeLevels,
    tags: [],
    download: null,
    structure: "functree",
  };
  const { data: ResourceSearchApiResource, isLoading } =
    useSearchResourcesQuery({
      body,
      page: null,
      limit: null,
    });

  const resources = (ResourceSearchApiResource?.data ??
    {}) as IResourceFunctree;

  if (!(resources && !lodash.isEmpty(resources) && resources[title])) {
    return <></>;
  }

  return (
    <ResourceAccordion
      title={title}
      resources={resources[title] as unknown as RecursiveDataSet}
      selectProps={createSelectProps(filterOptions)}
      favorites={favorites}
      profile={profile}
      isLoading={isLoading}
      getSelectValues={getSelectValues}
      exportFilters={exportFilters}
    />
  );
}
