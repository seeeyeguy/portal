import React from "react";
import { RecursiveAccordion } from "adas-react-components";

import FilterableResourceLinks from "components/links/FilterableResourceLinks";

import {
  RecursiveAccordionChildrenProps,
  ResourceAccordionProps,
} from "components/accordions/ResourceAccordion/types";

import styles from "components/accordions/ResourceAccordion/styles/index.module.css";

export default React.memo(function ResourceAccordion({
  title,
  resources,
  selectProps,
  favorites,
  profile,
  isLoading,
  getSelectValues,
  exportFilters,
}: ResourceAccordionProps) {
  return (
    <RecursiveAccordion
      title={title}
      dataSet={resources}
      isLoading={isLoading}
      spinner="moon"
      recursionDepth={0}
    >
      {(props: unknown) => {
        const containerId = (props as RecursiveAccordionChildrenProps)
          .childrenId;
        const containerProps = {
          favorites,
          profile,
        };
        const resources = (props as RecursiveAccordionChildrenProps).dataSet;

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
