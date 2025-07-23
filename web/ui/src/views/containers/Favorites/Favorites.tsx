import React from "react";
import { Tooltip } from "react-tooltip";
import { RecursiveAccordion } from "adas-react-components";
import type { RecursiveDataSet } from "adas-react-components/types";
import lodash from "lodash";
import { Button } from 'primereact/button';

import ResourceLinks from "views/components/ResourceLinks/ResourceLinks";

import { IFavorite } from "definitions/portal/preferences/Favorite.types";
import { IProfile } from "definitions/portal/users/Profile.types";

import styles from "views/containers/Favorites/Favorites.module.css";

enum ESortTypes {
  ADDED_DATE = 1,
  ALPHABETICAL = 2,
}

export interface IFavoritesProps {
  favorites: IFavorite[];
  profile: IProfile;
}

export default function Favorites({ favorites, profile }: IFavoritesProps) {
  const favoriteResources = favorites.map((item) => item.resource);

  const [sort, setSort] = React.useState<ESortTypes>(ESortTypes.ADDED_DATE);

  const sortedFavoriteResources = React.useMemo(() => {
    if (sort === ESortTypes.ALPHABETICAL) {
      return lodash.sortBy(favoriteResources, ['name']);
    }
    return favoriteResources;
  }, [favoriteResources, sort]);

  const handleSortChange = React.useCallback(() => {
    setSort((prevSort) =>
      prevSort === ESortTypes.ADDED_DATE
        ? ESortTypes.ALPHABETICAL
        : ESortTypes.ADDED_DATE
    );
  }, []);

  const tooltipText = React.useMemo(
    () =>
      sort === ESortTypes.ADDED_DATE
        ? "Sorted by add date."
        : "Sorted by alphabetical.",
    [sort]
  );

  return (
    <div
      className={styles["favorites"]}
      aria-description="container for favorite resources"
    >
      <section>
        <RecursiveAccordion
          title="Favorites"
          dataSet={sortedFavoriteResources as unknown as RecursiveDataSet}
          className={styles["favorite-accordion"]}
          spinner="moon"
          recursionDepth={0}
        >
          {() => (
            <div
              className={styles["favorites-resource-links-container"]}
              aria-description="container for favorite resource links"
            >
              {lodash.isEmpty(favorites) ? (
                <div
                  aria-description="empty container for favorite resource links"
                  className={styles["favorites-no-resources"]}
                >
                  No Favorites Selected
                </div>
              ) : (
                <>
                  <Button
                    className={styles["resource-sort"]}
                    onClick={handleSortChange}
                    data-tooltip-id="resource-favorite-sort-tooltip"
                    data-tooltip-delay-show={200}
                    icon={`pi ${sort === ESortTypes.ADDED_DATE ? 'pi-sort-numeric-down' : 'pi-sort-alpha-down'}`}
                  />
                  <Tooltip
                    id="resource-favorite-sort-tooltip"
                    className={styles["resource-sort-tooltip"]}
                    place={"top"}
                  >
                    {tooltipText}
                  </Tooltip>
                  <ResourceLinks
                    resources={sortedFavoriteResources}
                    favorites={favorites}
                    profile={profile}
                  />
                </>
              )}
            </div>
          )}
        </RecursiveAccordion>
      </section>
    </div>
  );
}
