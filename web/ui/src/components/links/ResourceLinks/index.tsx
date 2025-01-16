import React from "react";
import { PagedItemContainer } from "adas-react-components";

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

  return (
    <PagedItemContainer
      dataSet={createResourceCollection(
        resources,
        resourceFavoriteMap,
        profile
      )}
      className={styles["resource-links"]}
      {...rest}
    />
  );
}
