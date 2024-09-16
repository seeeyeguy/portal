import { ApiEmployeeLevel } from "routes/api/helpers/transforms/portal/response/directory/EmployeeLevel";
import { ApiSubFunction } from "routes/api/helpers/transforms/portal/response/directory/SubFunction";
import { ApiTag } from "routes/api/helpers/transforms/portal/response/directory/Tag";
import Resource from "state/types/portal/directory/Resource";
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

/**
 * Transforms a `portal.directory.Resource` record from snake_casing
 * to camelCasing.
 * @param data A `portal.directory.Resource` record.
 * @returns A `portal.directory.Resource` record with desired casing.
 */
export default function transformResourceRecord(data: ApiResource): Resource {
  return snakeCaseToCamelCase({ ...data }) as unknown as Resource;
}
