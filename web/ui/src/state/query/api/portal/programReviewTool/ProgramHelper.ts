import { IProgram } from "views/definitions/ProgramReviewTool.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiProgram {
  id: number;
  pa_number: string;
  name: string;
  segment: string;
  sector: string;
  division: string;
  tier: number;
  contract_value: number;
  active_status: boolean;
  created: Date;
  modified: Date;
}

/**
 * Transforms a `program_review_tool.Program` record from snake_casing
 * to camelCasing.
 * @param data A `program_review_tool.Program` record.
 * @returns A `program_review_tool.Program` record with desired casing.
 */
export function transformProgramRecord(data: IApiProgram): IProgram {
  return snakeCaseToCamelCase({ ...data }) as unknown as IProgram;
}
