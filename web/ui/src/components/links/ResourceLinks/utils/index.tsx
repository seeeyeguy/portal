import lodash from "lodash";

import ResourceLink from "components/links/ResourceLink";

import { ResourceFavoriteMap } from "components/links/ResourceLinks/types";

import Resource from "state/types/portal/directory/Resource";
import Profile from "state/types/portal/users/Profile";
import Segment from "state/types/portal/users/Segment";
import { User } from "state/types/services/sso";

const resourceTypeThumbnailPaths: { [key: string]: string } = {
  "command media": "command media/command_media_default_icon.png",
  excel: "excel/excel_default_icon.png",
  powerapps: "powerapps/powerapps_default_icon.png",
  powerbi: "powerbi/power-bi_default_icon.png",
  sharepoint: "sharepoint/sharepoint_default_icon.png",
  tableau: "tableau/Tableau_default_icon.png",
  "web link": "web link/weblink_black_default_icon.png",
};

/**
 * Returns the path for a resource's thumbnail based on
 * resource.thumbnail or resource.type, otherwise a default if neither exist.
 * @param resource A resource record.
 * @returns {string} A path to a thumbnail for the given resource.
 */
function getThumbnailPath(resource: Resource) {
  if (resource.thumbnail?.length) {
    return `/api${resource.thumbnail}`;
  }
  if (resource?.type?.toLowerCase() in resourceTypeThumbnailPaths) {
    return `/thumbnail/resourceTypes/${resourceTypeThumbnailPaths[resource.type.toLowerCase()]}`;
  }
  return "/thumbnail/default/l3harris_red_thumbnail.png";
}

/**
 * Create resource links, given a collection of resource records.
 * @param resources A collection of resource records, typically from an Api.
 * @param resourceFavoriteMap A map of records and their favorites, used to determine the
 * state of a ResourceLink's favorite button.
 * @param profile A profile record, used to determine a user's access to a resource.
 * @returns {ResourceLink[]} A collection of resource links.
 */
export const createResourceCollection = (
  resources: Resource[],
  resourceFavoriteMap: ResourceFavoriteMap,
  profile: Profile
) =>
  resources
    .filter((resource) =>
      lodash.keys(resource.restricted).every((key) => {
        if (resource.restricted && resource.restricted[key].length) {
          const typedKey = key as keyof Profile;
          const control =
            (profile[typedKey] as Segment)?.name ??
            (profile[typedKey] as User)?.email ??
            profile[typedKey];
          return key in profile && resource.restricted[key].includes(control);
        }
        return true;
      })
    )
    .map((resource) => (
      <ResourceLink
        id={resource.id}
        name={resource.name}
        description={resource.description}
        url={resource.url}
        thumbnail={getThumbnailPath(resource)}
        download={resource.download}
        favoriteId={resourceFavoriteMap[resource.id].favoriteId}
        key={resourceFavoriteMap[resource.id].id}
      />
    ));
