import React from "react";
import type { Filters, Option } from "adas-react-components/types";
import lodash from "lodash";

import Resources from "views/containers/Resources/Resources";

import { useGetFunctionsQuery } from "state/query/api/portal/directory/FunctionApi";
import { useTypedSelector } from "state/store/store";

import { IFunction } from "definitions/portal/directory/Function.types";
import { ITag } from "definitions/portal/directory/Tag.types";
import { IFavorite } from "definitions/portal/preferences/Favorite.types";
import { IProfile } from "definitions/portal/users/Profile.types";

import { transformToOption } from "views/utils/OptionsUtility";

import styles from "views/containers/Results/Results.module.css";

export interface IResultsProps {
  favorites: IFavorite[];
  filterData: React.MutableRefObject<{ [key: string]: string[] }>;
  filterTags: ITag[];
  profile: IProfile;
}

export default function Results({
  favorites,
  filterData,
  filterTags,
  profile,
}: IResultsProps) {
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
  const functions = (functionsApiResponse?.data ?? []) as IFunction[];

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
