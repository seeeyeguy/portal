import { IApiResource } from "state/query/api/portal/directory/ResourceHelper";
import {
  IApiUser,
  transformUserRecord,
} from "state/query/api/portal/users/UsersHelper";

import { IFavorite } from "definitions/portal/preferences/Favorite.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiFavorite {
  id: number;
  user: IApiUser;
  resource: IApiResource;
  rank: number;
  created: Date;
}

/**
 * Transforms a `portal.preferences.Favorite` record from snake_casing
 * to camelCasing.
 * @param data A `portal.preferences.Favorite` record.
 * @returns A `portal.preferences.Favorite` record with desired casing.
 */
export default function transformFavoriteRecord(data: IApiFavorite): IFavorite {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as IFavorite;
}
