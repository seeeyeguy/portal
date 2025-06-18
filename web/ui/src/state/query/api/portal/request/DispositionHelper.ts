import { IApiAccess } from "state/query/api/portal/users/AccessHelper";

import { IDisposition } from "definitions/portal/request/Disposition.types.ts";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiDisposition extends Omit<IDisposition, "approver"> {
  approver: IApiAccess;
}

/**
 * Transforms a `portal.request.Disposition` record from snake_casing
 * to camelCasing.
 * @param data A `portal.request.Disposition` record.
 * @returns A `portal.request.Disposition` record with desired casing.
 */
export function transformDispositionRecord(
  data: IApiDisposition
): IDisposition {
  return snakeCaseToCamelCase({ ...data }) as unknown as IDisposition;
}
