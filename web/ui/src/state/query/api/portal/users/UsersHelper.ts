import { transformApiUser as transformUserRecord } from "state/query/api/auth/AuthHelper";

import { IProfile, ISegment } from "definitions/portal/Users.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiSegment extends ISegment {}

export interface IApiUser {
  email: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
}

export interface IApiProfile {
  user: IApiUser;
  uid: string;
  middle_initial: string;
  unix_name: string;
  job_title: string;
  job_function: string;
  job_family: string;
  job_category: string;
  job_level: number;
  account_type: string;
  status: string;
  segment: IApiSegment;
  division: string;
  business_unit: string;
  department: string;
  location: string;
  citizenship: string;
}

/**
 * Transforms a `portal.users.Profile` record from snake_casing
 * to camelCasing.
 * @param data A `portal.users.Profile` record.
 * @returns A `portal.users.Profile` record with desired casing.
 */
export function transformProfileRecord(data: IApiProfile): IProfile {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as IProfile;
}

export { transformUserRecord };
