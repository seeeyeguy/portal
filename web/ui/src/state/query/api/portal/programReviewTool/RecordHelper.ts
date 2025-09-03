import { IRecord } from "views/definitions/ProgramReviewTool.types";

import { IApiProgram } from "state/query/api/portal/programReviewTool/ProgramHelper";
import { IApiUser } from "state/query/api/portal/users/UsersHelper";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

type TOmitIApiProgramProps = "active_status" | "modified";

export interface IApiRecord extends Omit<IApiProgram, TOmitIApiProgramProps> {
  previous_revision: number | null;
  program: IApiProgram;
  reporting_period: number;
  program_phase: string;
  site: string;
  defense_financial_acquisition_regulation_clause: boolean;
  cost_and_software_data_reporting_system_clause: boolean;
  earned_value_management_system_reporting_requirement: string;
  customer_assessment: number;
  technical_assessment: number;
  risk_assessment: number;
  overall_program: number;
  comments: string;
  user: IApiUser;
}

/**
 * Transforms a `program_review_tool.Record` record from snake_casing
 * to camelCasing.
 * @param data A `program_review_tool.Record` record.
 * @returns A `program_review_tool.Record` record with desired casing.
 */
export function transformRecordRecord(data: IApiRecord): IRecord {
  return snakeCaseToCamelCase({ ...data }) as unknown as IRecord;
}
