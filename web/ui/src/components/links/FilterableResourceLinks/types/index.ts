import type { Filters, SelectFilterProps } from "adas-react-components/types";

import { ResourceLinksProps } from "components/links/ResourceLinks/types";

import Resource from "state/types/portal/directory/Resource";

interface ResourceContainerProps
  extends Omit<ResourceLinksProps, "resources"> {}

export interface FilterableResourceLinksChildrenProps
  extends ResourceContainerProps {
  dataSet: Resource[];
}

export interface FilterableResourceLinksProps {
  id: string;
  resources: Resource[];
  selectProps: SelectFilterProps[];
  resourceContainerProps: ResourceContainerProps;
  exportFilters: (filters: Filters) => void;
}
