import React from "react";
import { PagedItemContainer } from "adas-react-components";
import lodash from "lodash";

import { TResourceFavoriteMap } from "views/definitions/ResourceLinks.types";
import { IResource } from "definitions/portal/directory/Resource.types";
import { IFavorite } from "definitions/portal/preferences/Favorite.types";
import { IProfile } from "definitions/portal/users/Users.types";

import { createResourceCollection } from "views/utils/ResourceLinksUtility";

import styles from "views/components/ResourceLinks/ResourceLinks.module.css";

export interface IResourceLinksProps {
  resources: IResource[];
  favorites: IFavorite[];
  profile: IProfile;
}

export default function ResourceLinks({
  resources,
  favorites,
  profile,
  ...rest
}: IResourceLinksProps) {
  // Create a memoized map to allow favorited links to be updated.
  const resourceFavoriteMap: TResourceFavoriteMap = React.useMemo(
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
      }, {} as TResourceFavoriteMap),
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
