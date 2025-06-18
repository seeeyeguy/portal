import { IApiSubFunction } from "state/query/api/portal//directory/SubFunctionHelper";
import { IApiStage } from "state/query/api/portal/request/StageHelper";
import { IApiRole } from "state/query/api/portal/users/RoleHelper";
import { IApiUser } from "state/query/api/portal/users/UsersHelper";

import { IAccess } from "definitions/portal/users/Access.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiAccess {
  id: number;
  user: IApiUser;
  role: IApiRole;
  stage: IApiStage[] | number[];
  subfunctions: IApiSubFunction[] | number[];
  access_granted_date: Date;
  access_revoked_date: Date | null;
}

/**
 * Transforms a `portal.users.Access` record from snake_casing
 * to camelCasing.
 * @param data A `portal.users.Access` record.
 * @returns A `portal.users.Access` record with desired casing.
 */
export function transformAccessRecord(data: IApiAccess): IAccess {
  return snakeCaseToCamelCase({ ...data }) as unknown as IAccess;
}
