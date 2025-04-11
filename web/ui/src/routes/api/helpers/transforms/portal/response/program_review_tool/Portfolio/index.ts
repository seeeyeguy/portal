import {
  ApiProgram,
  transformProgramRecord,
} from "routes/api/helpers/transforms/portal/response/program_review_tool/Program";
import { ApiUser } from "routes/api/helpers/transforms/services/sso";
import Portfolio from "state/types/program_review_tool/Portfolio";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

export interface ApiPortfolio {
  id: number;
  user: ApiUser;
  programs: ApiProgram[];
  name: string;
  created: Date;
  modified: Date;
}

/**
 * Transforms a `program_review_tool.Portfolio` record from snake_casing
 * to camelCasing.
 * @param data A `program_review_tool.Portfolio` record.
 * @returns A `program_review_tool.Portfolio` record with desired casing.
 */
export function transformPortfolioRecord(data: ApiPortfolio): Portfolio {
  const programs =
    data?.programs.map((program) => transformProgramRecord(program)) ?? [];
  return snakeCaseToCamelCase({ ...data, programs }) as unknown as Portfolio;
}
