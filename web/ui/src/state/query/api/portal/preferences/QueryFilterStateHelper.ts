import { IApiQuery } from "state/query/api/portal/analytics/AnalyticsHelper";
import {
  IApiUser,
  transformUserRecord,
} from "state/query/api/portal/users/UsersHelper";

import { IQueryFilterState } from "definitions/portal/preferences/QueryFilterState.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface ApiQueryFilterState {
  id: number;
  search: IApiQuery;
  user: IApiUser;
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
): IQueryFilterState {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as IQueryFilterState;
}
