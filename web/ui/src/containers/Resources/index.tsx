import lodash from "lodash";

import type { RecursiveDataSet } from "adas-react-components/types";

import ResourceAccordion from "components/accordions/ResourceAccordion";

import { ResourcesProps } from "containers/Resources/types";

import { createSelectProps } from "containers/Resources/utils";

import {
  useSearchResourcesQuery,
  ApiSearchResourceRequest,
} from "state/query/api/portal/directory/Resource";

import { ResourceFunctree } from "state/types/portal/directory/Resource";

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
}: ResourcesProps) {
  const body: ApiSearchResourceRequest = {
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

  const resources = (ResourceSearchApiResource?.data ?? {}) as ResourceFunctree;

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
