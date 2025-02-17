import React from "react";
import type { Filters, Option } from "adas-react-components/types";
import lodash from "lodash";

import Resources from "containers/Resources";

import { ResultsProps } from "containers/Results/types";

import { useGetFunctionsQuery } from "state/query/api/portal/directory/Function";
import { useTypedSelector } from "state/store";

import Function from "state/types/portal/directory/Function";

import { transformToOption } from "utils/components/select/options";

import styles from "containers/Results/styles/index.module.css";

export default function Results({
  favorites,
  filterData,
  filterTags,
  profile,
}: ResultsProps) {
  const employeeLevelIds = useTypedSelector(
    (state) => state.ResourceSearch.employeeLevels
  );
  const functionIds = useTypedSelector(
    (state) => state.ResourceSearch.functions
  );
  const searchTerm = useTypedSelector(
    (state) => state.ResourceSearch.search.term
  );

  const { data: functionsApiResponse } = useGetFunctionsQuery(null);
  const functions = (functionsApiResponse?.data ?? []) as Function[];

  const filterOptions = React.useMemo(
    () =>
      filterTags.reduce(
        (acc, record) => {
          const filterLabel = record.label.slice(8);
          const [filterName, filterValue] = filterLabel.split(":");
          if (!(filterName in acc)) {
            acc[filterName] = [];
          }
          return {
            ...acc,
            [filterName]: [...acc[filterName], transformToOption(filterValue)],
          };
        },
        {} as { [key: string]: Option[] }
      ),
    [filterTags]
  );

  const getSelectValues = React.useCallback(
    (id: string) =>
      filterData.current[id]?.map((filterValue) =>
        transformToOption(filterValue)
      ) ?? [],
    [filterData]
  );

  const exportFilters = React.useCallback(
    (id: string) => (filters: Filters) => {
      const selectValuesEntries = lodash.entries(filters).reduce(
        (acc, [filterName, filterValues]) => ({
          ...acc,
          [`${id}-${filterName}`]: filterValues,
        }),
        {}
      );
      filterData.current = {
        ...filterData.current,
        ...selectValuesEntries,
      };
    },
    [filterData]
  );

  return (
    <div
      className={styles["resource-search-results"]}
      aria-description="results for resource search"
    >
      {functions
        .filter(
          (record) => !functionIds?.length || functionIds.includes(record.id)
        )
        .map((record) => (
          <section key={record.id}>
            <Resources
              title={record.name}
              searchTerm={searchTerm}
              employeeLevels={employeeLevelIds}
              functions={[record.id]}
              favorites={favorites}
              profile={profile}
              filterOptions={filterOptions}
              getSelectValues={getSelectValues}
              exportFilters={exportFilters}
            />
          </section>
        ))}
    </div>
  );
}
