import { RecursiveAccordion } from "adas-react-components";
import type { RecursiveDataSet } from "adas-react-components/types";
import lodash from "lodash";

import ResourceLinks from "views/components/ResourceLinks/ResourceLinks";

import { IFavorite } from "definitions/portal/preferences/Favorite.types";
import { IProfile } from "definitions/portal/users/Users.types";

import styles from "views/containers/Favorites/Favorites.module.css";

export interface IFavoritesProps {
  favorites: IFavorite[];
  profile: IProfile;
}

export default function Favorites({ favorites, profile }: IFavoritesProps) {
  const favoriteResources = favorites.map((item) => item.resource);

  return (
    <div
      className={styles["favorites"]}
      aria-description="container for favorite resources"
    >
      <section>
        <RecursiveAccordion
          title="Favorites"
          dataSet={favoriteResources as unknown as RecursiveDataSet}
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
                <ResourceLinks
                  resources={favoriteResources}
                  favorites={favorites}
                  profile={profile}
                />
              )}
            </div>
          )}
        </RecursiveAccordion>
      </section>
    </div>
  );
}
