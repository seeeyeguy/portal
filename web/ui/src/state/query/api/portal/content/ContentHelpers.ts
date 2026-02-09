import { IContent } from "definitions/portal/content/Content.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiContent extends Omit<IContent, "modifiedBy"> {
  modified_by: string;
}

/**
 * Transforms a `portal.content.Content` record from snake_casing
 * to camelCasing.
 * @param data A `portal.content.Content` record.
 * @returns A `portal.content.Content` record with desired casing.
 */
export function transformContentRecord(data: IApiContent): IContent {
  return snakeCaseToCamelCase({ ...data }) as unknown as IContent;
}
