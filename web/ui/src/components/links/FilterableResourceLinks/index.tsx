import React from "react";
import { FilterContainer } from "adas-react-components";
import type { Records, SelectFilterProps } from "adas-react-components/types";

import ResourceLinks from "components/links/ResourceLinks";

import {
  FilterableResourceLinksChildrenProps,
  FilterableResourceLinksProps,
} from "components/links/FilterableResourceLinks/types";

import Resource from "state/types/portal/directory/Resource";

export default function FilterableResourceLinks({
  id,
  resources,
  selectProps,
  resourceContainerProps,
  exportFilters,
}: FilterableResourceLinksProps) {
  const computedSelectProps = React.useMemo(
    () =>
      selectProps.reduce((acc: SelectFilterProps[], prop) => {
        // Get the filter key from the select filter prop.
        // The filter key is also a key on the `Resource` data object
        // that relates to its filterable values.
        const filterKey = prop.field as keyof Resource;
        // Create a set of unique filter values related to the `Resource`
        // data collection passed to this component.
        const resourceFilters = new Set(
          resources.reduce((acc: string[], resource) => {
            const filterValues = resource[filterKey] as string[];
            return [...acc, ...filterValues];
          }, [])
        );
        // Use those filter values obtained above to filter out
        // any select filter options that do not relate to the `Resource`
        // data collection passed to this component.
        const validOptions = prop.options.filter((option) =>
          resourceFilters.has(option.value as unknown as string)
        );
        // Substitute the options for the current select filter prop
        // object with the new filtered collection of options.
        const computedSelectProp = {
          ...prop,
          options: validOptions,
        };
        return [...acc, computedSelectProp];
      }, []),
    [resources, selectProps]
  );

  // Compute the number of options related to the `Resource` data collection
  // passed to this component. If the total is 0, render the component without
  // the filter container.
  if (
    !computedSelectProps.reduce(
      (acc: number, prop: SelectFilterProps) => acc + prop.options.length,
      0
    )
  ) {
    return <ResourceLinks resources={resources} {...resourceContainerProps} />;
  }

  return (
    <FilterContainer
      id={id}
      dataSet={resources as unknown as Records}
      selectProps={computedSelectProps}
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
