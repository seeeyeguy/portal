import Program from "state/types/program_review_tool/Program";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

export interface ApiProgram {
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
export function transformProgramRecord(data: ApiProgram): Program {
  return snakeCaseToCamelCase({ ...data }) as unknown as Program;
}
