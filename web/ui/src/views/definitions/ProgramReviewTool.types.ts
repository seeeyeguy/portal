import { IUser } from "definitions/portal/users/User.types";

export const REPORTING_PERIOD_CONTENT_KEY = "ADMIN_REPORTING_PERIOD_PPR";

export const DEFAULT_PORTFOLIO_ID = -1;

export enum assessmentOptions {
  RED = 1,
  YELLOW = 2,
  GREEN = 3,
  BLUE = 4,
}

export enum EReviewStatus {
  SUBMITTED = -2,
  ERROR = -1,
  QUEUED = 0,
  PROCESSING = 1,
  COMPLETE = 2,
}

export interface IProgramRole {
  id: number;
  name: string;
  description: string;
  created: Date;
  modified: Date;
}

export interface IProgramMember {
  id: number;
  program: number;
  role: IProgramRole;
  user: IUser;
  created: Date;
  expiryDate: Date | null;
  modified: Date;
}

export interface IProgram {
  id: number;
  paNumber: string;
  name?: string;
  segment?: string;
  sector?: string;
  division?: string;
  tier?: number | null;
  contractType: string | null;
  contractNumber: string | null;
  contractValue?: number | null;
  contractStartDate: string | null;
  contractEndDate: string | null;
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
  activeStatus: boolean;
  teamMembers: IProgramMember[];
  isManualMetricsEntry: boolean | null;
  created: string;
  modified: string;
  disabled: boolean;
}

export interface IPrograms {
  [key: string]: IProgram;
}

export interface IPortfolio {
  id: number;
  user?: IUser;
  programs: IPrograms;
  name: string;
  created: string;
  modified: string;
}

export interface IPortfolios {
  [key: number]: IPortfolio;
}

export interface IPortfolioMetadata {
  id: number;
  name: string;
  modified: string;
  numberOfPrograms: number;
}

type TOmitIProgramProps = "activeStatus" | "modified" | "disabled";

export interface ITask {
  id: number | null;
  paNumber: string | null;
  reportingPeriod: number | null;
  order: number | null;
  name: string | null;
  description: string | null;
  owner: string | null;
  status: string | null;
  createDate: string;
  targetDate: string | null;
  completeDate: string | null;
  archiveDate: string | null;
}

export interface IRecord extends Omit<IProgram, TOmitIProgramProps> {
  previousRevision: number | null;
  program: IProgram;
  reportingPeriod: number;
  programPhase: string;
  site: string;
  defenseFinancialAcquisitionRegulationClause: boolean;
  costAndSoftwareDataReportingSystemClause: boolean;
  earnedValueManagementSystemReportingRequirement: string;
  customerAssessment: number;
  technicalAssessment: number;
  riskAssessment: number;
  overallProgram: number;
  comments: string;
  user: IUser;
  tasks: ITask[];
}

export interface IJobRun {
    id: number;
    jobName: string;
    status: "PENDING" | "RUNNING" | "SUCCESS" | "FAILURE"
    user: string;
    started_at: string | null;
    finished_at: string | null;
    duration: string | null;
    error_msg: string | null;
    created_at: string | null;
}

export interface IJobRegistryJob {
    name: string;
    description: string;
}
