import { POST } from "definitions/RequestConstants";
import endpoints from "services/api";
import api from "state/query/api";
import {
  IApiRecord,
  transformRecordRecord,
} from "state/query/api/portal/programReviewTool/RecordHelper";

import { IRecord } from "views/definitions/ProgramReviewTool.types";

type TApiRecordResponse = {
  data: IRecord;
  status: number | undefined;
};

export type TApiPostRecordRequest = {
  paNumber: string;
  reportingPeriod: number;
  name: string;
  segment: string;
  sector: string;
  division: string;
  tier: number | null;
  programPhase: string;
  site: string;
  defenseFinancialAcquisitionRegulationClause: boolean | null;
  costAndSoftwareDataReportingSystemClause: boolean | null;
  earnedValueManagementSystemReportingRequirement: string;
  contractType: string;
  contractNumber: string;
  contractValue: number | null;
  contractStartDate: Date | null;
  contractEndDate: Date | null;
  actualCostWorkPerformedCumulative: number | null;
  budgetedCostWorkPerformedCumulative: number | null;
  budgetedCostWorkScheduledCumulative: number | null;
  costPerformanceIndexCumulative: number | null;
  schedulePerformanceIndexCumulative: number | null;
  budgetAtComplete: number | null;
  estimateAtComplete: number | null;
  estimateToComplete: number | null;
  managementReserve: number | null;
  weightedRisksAndOpportunities: number | null;
  customerAssessment: number | null;
  technicalAssessment: number | null;
  riskAssessment: number | null;
  overallProgram: number | null;
  comments: string;
};

export type TApiFetchRecordRequest = {
  paNumber: string;
  reportingPeriod: number;
  refresh: boolean;
};

const recordApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addRecord: builder.mutation<TApiRecordResponse, TApiPostRecordRequest>({
      query: (body: TApiPostRecordRequest) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.RECORD(),
        method: POST,
        body: {
          pa_number: body.paNumber,
          reporting_period: body.reportingPeriod,
          name: body.name,
          segment: body.segment,
          sector: body.sector,
          division: body.division,
          tier: body.tier,
          program_phase: body.programPhase,
          site: body.site,
          defense_financial_acquisition_regulation_clause:
            body.defenseFinancialAcquisitionRegulationClause,
          cost_and_software_data_reporting_system_clause:
            body.costAndSoftwareDataReportingSystemClause,
          earned_value_management_system_reporting_requirement:
            body.earnedValueManagementSystemReportingRequirement,
          contract_type: body.contractType,
          contract_number: body.contractNumber,
          contract_value: body.contractValue,
          contract_start_date: body.contractStartDate,
          contract_end_date: body.contractEndDate,
          actual_cost_work_performed_cumulative:
            body.actualCostWorkPerformedCumulative,
          budgeted_cost_work_performed_cumulative:
            body.budgetedCostWorkPerformedCumulative,
          budgeted_cost_work_scheduled_cumulative:
            body.budgetedCostWorkScheduledCumulative,
          cost_performance_index_cumulative:
            body.costPerformanceIndexCumulative,
          schedule_performance_index_cumulative:
            body.schedulePerformanceIndexCumulative,
          budget_at_complete: body.budgetAtComplete,
          estimate_at_complete: body.estimateAtComplete,
          estimate_to_complete: body.estimateToComplete,
          management_reserve: body.managementReserve,
          weighted_risks_and_opportunities: body.weightedRisksAndOpportunities,
          customer_assessment: body.customerAssessment,
          technical_assessment: body.technicalAssessment,
          risk_assessment: body.riskAssessment,
          overall_program: body.overallProgram,
          comments: body.comments,
        },
      }),
      transformResponse: (response: IApiRecord, meta): TApiRecordResponse => ({
        data: transformRecordRecord(response),
        status: meta?.response?.status,
      }),
    }),
    getRecord: builder.query<TApiRecordResponse, TApiFetchRecordRequest>({
      query: ({ paNumber, reportingPeriod, refresh }: TApiFetchRecordRequest) =>
        endpoints.PORTAL.PROGRAM_REVIEW_TOOL.RECORD(
          paNumber,
          reportingPeriod,
          refresh
        ),
      transformResponse: (response: IApiRecord, meta): TApiRecordResponse => ({
        data: transformRecordRecord(response),
        status: meta?.response?.status,
      }),
    }),
  }),
});

export default recordApi;
export const { useAddRecordMutation, useGetRecordQuery } = recordApi;
