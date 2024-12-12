import { PagedItemContainer } from "adas-react-components";

import { ResourceLinksProps } from "components/links/ResourceLinks/types";

import { createResourceCollection } from "components/links/ResourceLinks/utils";

import styles from "components/links/ResourceLinks/styles/index.module.css";

export default function ResourceLinks({
  resources,
  favorites,
  profile,
  ...rest
}: ResourceLinksProps) {
  return (
    <PagedItemContainer
      dataSet={createResourceCollection(resources, favorites, profile)}
      className={styles["resource-links"]}
      {...rest}
    />
  );
}
