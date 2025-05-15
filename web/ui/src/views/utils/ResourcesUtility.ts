import lodash from "lodash";

import { IFilterOptions } from "views/definitions/Resources.types";

export function createSelectProps(filterOptions: IFilterOptions) {
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
