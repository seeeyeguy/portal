import { IProfile, ISegment } from "definitions/portal/users/Profile.types";
import { IUser } from "definitions/portal/users/User.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiSegment extends ISegment {}

export interface IApiUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
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
 * Transforms a `portal.users.User` record from snake_casing
 * to camelCasing.
 * @param data A `portal.users.User` record.
 * @returns A `portal.users.User` record with desired casing.
 */
export function transformUserRecord(data: IApiUser): IUser {
  return {
    ...snakeCaseToCamelCase({ ...data }),
  } as unknown as IUser;
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
