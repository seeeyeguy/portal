import { ApiSegment } from "routes/api/helpers/transforms/portal/response/users/Segment";
import transformUserRecord, {
  ApiUser,
} from "routes/api/helpers/transforms/portal/response/users/User";

import Profile from "state/types/portal/users/Profile";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

export interface ApiProfile {
  user: ApiUser;
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
  segment: ApiSegment;
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
export default function transformProfileRecord(data: ApiProfile): Profile {
  return {
    ...snakeCaseToCamelCase({ ...data }),
    user: transformUserRecord(data.user),
  } as unknown as Profile;
}
