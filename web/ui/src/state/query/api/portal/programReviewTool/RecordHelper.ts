import { IRecord, ITask } from "views/definitions/ProgramReviewTool.types";

import { IApiProgram } from "state/query/api/portal/programReviewTool/ProgramHelper";
import { IApiUser } from "state/query/api/portal/users/UsersHelper";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

type TOmitIApiProgramProps = "active_status" | "modified";

export interface IApiTask {
  id: number | null;
  pa_number: string;
  reporting_period: number[];
  order: number | null;
  name: string;
  description: string;
  owner: string;
  status: string;
  create_date: string;
  target_date: string;
  complete_date: string | null;
  archive_date: string | null;
}

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
  tasks: IApiTask[];
}

/**
 * Transforms a `program_review_tool.Task` record from snake_casing
 * to camelCasing.
 * @param data A `program_review_tool.Task` record.
 * @returns A `program_review_tool.Task` record with desired casing and types.
 */
export function transformTaskRecord(data: IApiTask): ITask {
  return snakeCaseToCamelCase({
    ...data,
  }) as unknown as ITask;
}

/**
 * Transforms a `program_review_tool.Record` record from snake_casing
 * to camelCasing.
 * @param data A `program_review_tool.Record` record.
 * @returns A `program_review_tool.Record` record with desired casing.
 */
export function transformRecordRecord(data: IApiRecord): IRecord {
  return snakeCaseToCamelCase({
    ...data,
    tasks: data.tasks?.map(transformTaskRecord) ?? [],
  }) as unknown as IRecord;
}
