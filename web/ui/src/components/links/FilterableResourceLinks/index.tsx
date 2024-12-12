import { FilterContainer } from "adas-react-components";
import type { Records } from "adas-react-components/types";

import ResourceLinks from "components/links/ResourceLinks";

import {
  FilterableResourceLinksChildrenProps,
  FilterableResourceLinksProps,
} from "components/links/FilterableResourceLinks/types";

export default function FilterableResourceLinks({
  id,
  resources,
  selectProps,
  resourceContainerProps,
  exportFilters,
}: FilterableResourceLinksProps) {
  return (
    <FilterContainer
      id={id}
      dataSet={resources as unknown as Records}
      selectProps={selectProps}
      containerProps={resourceContainerProps}
      exportFilters={exportFilters}
    >
      {(props: unknown) => {
        const { dataSet, ...rest } =
          props as FilterableResourceLinksChildrenProps;
        return <ResourceLinks resources={dataSet} {...rest} />;
      }}
    </FilterContainer>
  );
}
