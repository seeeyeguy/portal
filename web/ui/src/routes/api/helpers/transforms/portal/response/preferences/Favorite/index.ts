import { ApiResource } from "routes/api/helpers/transforms/portal/response/directory/Resource";
import transformUserRecord, {
  ApiUser,
} from "routes/api/helpers/transforms/portal/response/users/User";
import Favorite from "state/types/portal/preferences/Favorite";
import { snakeCaseToCamelCase } from "utils/transforms/helpers";

export interface ApiFavorite {
  id: number;
  user: ApiUser;
  resource: ApiResource;
  rank: number;
  created: Date;
}

/**
 * Transforms a `portal.preferences.Favorite` record from snake_casing
 * to camelCasing.
 * @param data A `portal.preferences.Favorite` record.
 * @returns A `portal.preferences.Favorite` record with desired casing.
 */
export default function transformFavoriteRecord(data: ApiFavorite): Favorite {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as Favorite;
}
