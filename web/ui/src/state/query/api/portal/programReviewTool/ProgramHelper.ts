import {
  IProgram,
  IProgramMember,
  IProgramRole,
} from "views/definitions/ProgramReviewTool.types";

import { IApiUser } from "state/query/api/portal/users/UsersHelper";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiProgramRole extends IProgramRole {}

export interface IApiProgramMember
  extends Omit<IProgramMember, "role" | "user" | "isActive" | "expiryDate"> {
  role: IApiProgramRole;
  user: IApiUser;
  is_active: boolean;
  expiry_date: Date | null;
}

export interface IApiProgram {
  id: number;
  pa_number: string;
  name: string;
  segment: string;
  sector: string;
  division: string;
  tier: number | null;
  contract_type: string;
  contract_number: string;
  contract_value: number | null;
  contract_start_date: Date | null;
  contract_end_date: Date | null;
  actual_cost_work_performed_cumulative: number | null;
  budgeted_cost_work_performed_cumulative: number | null;
  budgeted_cost_work_scheduled_cumulative: number | null;
  cost_performance_index_cumulative: number | null;
  schedule_performance_index_cumulative: number | null;
  budget_at_complete: number | null;
  estimate_at_complete: number | null;
  estimate_to_complete: number | null;
  management_reserve: number | null;
  weighted_risks_and_opportunities: number | null;
  active_status: boolean;
  team_members: IApiProgramMember[];
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
