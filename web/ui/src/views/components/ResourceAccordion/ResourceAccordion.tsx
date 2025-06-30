import React from "react";
import { RecursiveAccordion } from "adas-react-components";

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
        const resources = (props as IRecursiveAccordionChildrenProps).dataSet;

        return (
          <div
            className={styles["filterable-resource-links-container"]}
            aria-description="container for filterable resource links"
          >
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
