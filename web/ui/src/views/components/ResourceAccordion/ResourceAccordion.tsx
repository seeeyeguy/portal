import React from "react";
import { Tooltip } from "react-tooltip";
import { RecursiveAccordion } from "adas-react-components";
import lodash from "lodash";
import { Button } from "primereact/button";

import FilterableResourceLinks from "views/components/FilterableResourceLinks/FilterableResourceLinks";

import type {
  Filters,
  Option,
  RecursiveDataSet,
  SelectFilterProps,
} from "adas-react-components/types";
import { IResource } from "definitions/portal/directory/Resource.types";
import { IFavorite } from "definitions/portal/preferences/Favorite.types";
import { IProfile } from "definitions/portal/users/Profile.types";

import styles from "views/components/ResourceAccordion/ResourceAccordion.module.css";

enum ESortTypes {
  POPULARITY = 1,
  ALPHABETICAL = 2,
}

export interface IRecursiveAccordionChildrenProps {
  childrenId: string;
  dataSet: IResource[];
}

export interface IResourceAccordionProps {
  title: string;
  resources: RecursiveDataSet;
  selectProps: SelectFilterProps[];
  favorites: IFavorite[];
  profile: IProfile;
  isLoading: boolean;
  getSelectValues: (id: string) => Option[];
  exportFilters: (id: string) => (filters: Filters) => void;
}

export default React.memo(function ResourceAccordion({
  title,
  resources,
  selectProps,
  favorites,
  profile,
  isLoading,
  getSelectValues,
  exportFilters,
}: IResourceAccordionProps) {
  const [sort, setSort] = React.useState<ESortTypes>(ESortTypes.POPULARITY);

  const handleSortChange = React.useCallback(() => {
    setSort((prevSort) =>
      prevSort === ESortTypes.POPULARITY
        ? ESortTypes.ALPHABETICAL
        : ESortTypes.POPULARITY
    );
  }, []);

  return (
    <RecursiveAccordion
      title={title}
      dataSet={resources}
      isLoading={isLoading}
      spinner="moon"
      recursionDepth={0}
    >
      {(props: unknown) => {
        const containerId = (props as IRecursiveAccordionChildrenProps)
          .childrenId;
        const containerProps = {
          favorites,
          profile,
        };

        let resources = (props as IRecursiveAccordionChildrenProps).dataSet;

        // Sort resources if alphabetical sort is selected.
        if (sort === ESortTypes.ALPHABETICAL) {
          resources = lodash.sortBy(resources, ['name']);
        }

        const tooltipText =
          sort === ESortTypes.POPULARITY
            ? "Sorted by popularity."
            : "Sorted by alphabetical.";
            
        return (
          <div
            className={styles["filterable-resource-links-container"]}
            aria-description="container for filterable resource links"
          >
            <Button
              className={styles["resource-sort"]}
              onClick={handleSortChange}
              data-tooltip-id={`resource-${containerId}-sort-tooltip`}
              data-tooltip-delay-show={200}
              icon={`pi ${sort === ESortTypes.POPULARITY ? 'pi-sort-numeric-down' : 'pi-sort-alpha-down'}`}
            />
            <Tooltip
              id={`resource-${containerId}-sort-tooltip`}
              className={styles["resource-sort-tooltip"]}
              place={"top"}
            >
              {tooltipText}
            </Tooltip>
            <FilterableResourceLinks
              id={containerId}
              resources={resources}
              selectProps={selectProps.map((selectAttr) => ({
                ...selectAttr,
                id: `${containerId}-${selectAttr.id}`,
                name: `${containerId}-${selectAttr.name}`,
                inputId: `${containerId}-${selectAttr.inputId}`,
                values: getSelectValues(`${containerId}-${selectAttr.name}`),
              }))}
              resourceContainerProps={containerProps}
              exportFilters={exportFilters(containerId)}
            />
          </div>
        );
      }}
    </RecursiveAccordion>
  );
});
