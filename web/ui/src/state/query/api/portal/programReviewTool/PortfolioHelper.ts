import {
  IApiProgram,
  transformProgramRecord,
} from "state/query/api/portal/programReviewTool/ProgramHelper";
import { IApiUser } from "state/query/api/portal/users/UsersHelper";

import { IPortfolio } from "views/definitions/ProgramReviewTool.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiPortfolio {
  id: number;
  user: IApiUser;
  programs: IApiProgram[];
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
export function transformPortfolioRecord(data: IApiPortfolio): IPortfolio {
  const programs =
    data?.programs.map((program) => transformProgramRecord(program)) ?? [];
  return snakeCaseToCamelCase({ ...data, programs }) as unknown as IPortfolio;
}
