import { ApiResource } from "routes/api/helpers/transforms/portal/response/directory/Resource";
import transformUserRecord, {
  ApiUser,
} from "routes/api/helpers/transforms/portal/response/users/User";

import Visit from "state/types/portal/analytics/Visit";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

export interface ApiVisit {
  id: number;
  user: ApiUser;
  resource: ApiResource;
  created: Date;
}

/**
 * Transforms a `portal.analytics.Visit` record from snake_casing
 * to camelCasing.
 * @param data A `portal.analytics.Visit` record.
 * @returns A `portal.analytics.Visit` record with desired casing.
 */
export default function transformVisitRecord(data: ApiVisit) {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as Visit;
}
