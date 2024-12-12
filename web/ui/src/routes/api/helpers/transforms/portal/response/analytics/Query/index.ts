import { ApiResource } from "routes/api/helpers/transforms/portal/response/directory/Resource";
import transformUserRecord, {
  ApiUser,
} from "routes/api/helpers/transforms/portal/response/users/User";

import Query from "state/types/portal/analytics/Query";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

export interface ApiQuery {
  id: number;
  user: ApiUser;
  search_term: string;
  resources?: ApiResource[];
  created: Date;
}

/**
 * Transforms a `portal.analytics.Query` record from snake_casing
 * to camelCasing.
 * @param data A `portal.analytics.Query` record.
 * @returns A `portal.analytics.Query` record with desired casing.
 */
export default function transformQueryRecord(data: ApiQuery): Query {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as Query;
}
