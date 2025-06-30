import { IApiResource } from "state/query/api/portal/directory/ResourceHelper";
import {
  IApiUser,
  transformUserRecord,
} from "state/query/api/portal/users/UsersHelper";

import { IQuery, IVisit } from "definitions/portal/Analytics.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiQuery {
  id: number;
  user: IApiUser;
  search_term: string;
  resources?: IApiResource[];
  created: Date;
}

/**
 * Transforms a `portal.analytics.Query` record from snake_casing
 * to camelCasing.
 * @param data A `portal.analytics.Query` record.
 * @returns A `portal.analytics.Query` record with desired casing.
 */
export function transformQueryRecord(data: IApiQuery): IQuery {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as IQuery;
}

export interface IApiVisit {
  id: number;
  user: string;
  resource: IApiResource;
  created: Date;
}

/**
 * Transforms a `portal.analytics.Visit` record from snake_casing
 * to camelCasing.
 * @param data A `portal.analytics.Visit` record.
 * @returns A `portal.analytics.Visit` record with desired casing.
 */
export function transformVisitRecord(data: IApiVisit) {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: data.user,
  } as unknown as IVisit;
}
