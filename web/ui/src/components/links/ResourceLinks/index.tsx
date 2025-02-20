import React from "react";
import { PagedItemContainer } from "adas-react-components";
import lodash from "lodash";

import {
  ResourceFavoriteMap,
  ResourceLinksProps,
} from "components/links/ResourceLinks/types";

import { createResourceCollection } from "components/links/ResourceLinks/utils";

import styles from "components/links/ResourceLinks/styles/index.module.css";

export default function ResourceLinks({
  resources,
  favorites,
  profile,
  ...rest
}: ResourceLinksProps) {
  // Create a memoized map to allow favorited links to be updated.
  const resourceFavoriteMap: ResourceFavoriteMap = React.useMemo(
    () =>
      resources.reduce((acc, resource) => {
        // Find the corresponding favorite by resource ID.
        const favorite = favorites.find(
          (fav) => fav.resource.id === resource.id
        );
        acc[resource.id] = {
          id: `${resource.id}-${favorite?.id || "none"}`,
          favoriteId: favorite?.id || null,
        };
        return acc;
      }, {} as ResourceFavoriteMap),
    [favorites, resources]
  );

  const resourceCollection = React.useMemo(
    () => createResourceCollection(resources, resourceFavoriteMap, profile),
    [resources, resourceFavoriteMap, profile]
  );

  return (
    <>
      {lodash.isEmpty(resourceCollection) ? (
        <div
          className={styles["no-resources"]}
          aria-description="empty container for resource links"
        >
          No Links Available
        </div>
      ) : (
        <PagedItemContainer
          dataSet={resourceCollection}
          className={styles["resource-links"]}
          minColumnWidth={12.5}
          {...rest}
        />
      )}
    </>
  );
}
