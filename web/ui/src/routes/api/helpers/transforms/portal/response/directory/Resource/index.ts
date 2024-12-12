import lodash from "lodash";

import { ApiEmployeeLevel } from "routes/api/helpers/transforms/portal/response/directory/EmployeeLevel";
import { ApiSubFunction } from "routes/api/helpers/transforms/portal/response/directory/SubFunction";
import { ApiTag } from "routes/api/helpers/transforms/portal/response/directory/Tag";

import Resource, {
  ResourceRecords,
} from "state/types/portal/directory/Resource";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

interface Restricted {
  [key: string]: string;
}

export interface ApiResource {
  id: number;
  uid: string;
  previous_revision: number;
  revision_number: number;
  name: string;
  description: string;
  url: string;
  thumbnail: string;
  employee_levels: ApiEmployeeLevel[];
  subfunctions: ApiSubFunction[];
  tags: ApiTag[];
  type: string;
  download: boolean;
  active: boolean;
  created: Date;
  favorited_by: string[];
  restricted?: Restricted;
  site: string[];
}

export interface ApiResourceFunctreeResponse {
  [key: string]: ApiResource[] | ApiResourceFunctreeResponse;
}

/**
 * Transforms a `portal.directory.Resource` record from snake_casing
 * to camelCasing.
 * @param data A `portal.directory.Resource` record.
 * @returns A `portal.directory.Resource` record with desired casing.
 */
export function transformResourceRecord(data: ApiResource): Resource {
  return snakeCaseToCamelCase({ ...data }) as unknown as Resource;
}

/**
 * Transforms `portal.directory.Resource` records from snake_casing
 * to camelCasing.
 * @param data A `portal.directory.Resource` collection or functree.
 * @returns A `portal.directory.Resource` dataset with desired casing.
 */
export function transformResourceRecords(
  data: ApiResourceFunctreeResponse | ApiResource[]
): ResourceRecords {
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
