import lodash from "lodash";

import { FilterOptions } from "containers/Resources/types";

export function createSelectProps(filterOptions: FilterOptions) {
  return lodash.entries(filterOptions).map(([label, options]) => ({
    id: `${label}-filter-select`,
    label: `${label.at(0)?.toUpperCase()}${label.slice(1).toLowerCase()}`,
    field: label,
    options,
    name: label,
    inputId: label,
    values: [],
    setFilter: () => null,
    disabled: false,
    horizontal: true,
    className: "",
  }));
}
