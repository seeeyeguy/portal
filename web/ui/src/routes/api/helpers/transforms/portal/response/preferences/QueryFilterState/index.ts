import { ApiQuery } from "routes/api/helpers/transforms/portal/response/analytics/Query";
import transformUserRecord, {
  ApiUser,
} from "routes/api/helpers/transforms/portal/response/users/User";

import QueryFilterState from "state/types/portal/preferences/QueryFilterState";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

export interface ApiQueryFilterState {
  id: number;
  search: ApiQuery;
  user: ApiUser;
  functions: number[];
  employee_levels: number[];
  tags: number[];
  created: Date;
  modified: Date;
}

/**
 * Transforms a `portal.preferences.QueryFilterState` record from snake_casing
 * to camelCasing.
 * @param data A `portal.preferences.QueryFilterState` record.
 * @returns A `portal.preferences.QueryFilterState` record with desired casing.
 */
export default function transformQueryFilterStateRecord(
  data: ApiQueryFilterState
): QueryFilterState {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as QueryFilterState;
}
