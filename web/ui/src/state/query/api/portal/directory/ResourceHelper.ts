import lodash from "lodash";

import { IApiEmployeeLevel } from "state/query/api/portal/directory/EmployeeLevelHelper";
import { IApiSubFunction } from "state/query/api/portal/directory/SubFunctionHelper";
import { IApiTag } from "state/query/api/portal/directory/TagHelper";

import {
  IResource,
  TResourceRecords,
} from "definitions/portal/directory/Resource.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

interface IRestricted {
  [key: string]: string;
}

export interface IApiResource {
  id: number;
  uid: string;
  previous_revision: number;
  revision_number: number;
  name: string;
  description: string;
  url: string;
  thumbnail: string;
  primary_point_of_contact: string;
  employee_levels: IApiEmployeeLevel[];
  subfunctions: IApiSubFunction[];
  tags: IApiTag[];
  type: string;
  download: boolean;
  active: boolean;
  created: Date;
  favorited_by: string[];
  restricted?: IRestricted;
  site: string[];
}

export interface ApiResourceFunctreeResponse {
  [key: string]: IApiResource[] | ApiResourceFunctreeResponse;
}

/**
 * Transforms a `portal.directory.Resource` record from snake_casing
 * to camelCasing.
 * @param data A `portal.directory.Resource` record.
 * @returns A `portal.directory.Resource` record with desired casing.
 */
export function transformResourceRecord(data: IApiResource): IResource {
  return snakeCaseToCamelCase({ ...data }) as unknown as IResource;
}

/**
 * Transforms `portal.directory.Resource` records from snake_casing
 * to camelCasing.
 * @param data A `portal.directory.Resource` collection or functree.
 * @returns A `portal.directory.Resource` dataset with desired casing.
 */
export function transformResourceRecords(
  data: ApiResourceFunctreeResponse | IApiResource[]
): TResourceRecords {
  if (lodash.isArray(data)) {
    return data.map((record) => transformResourceRecord(record));
  }
  return lodash.entries(data).reduce(
    (acc, [key, value]) => ({
      ...acc,
      [key]: transformResourceRecords(value),
    }),
    {}
  );
}
