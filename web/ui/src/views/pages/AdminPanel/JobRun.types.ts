/**
 * TypeScript types for the JobRun feature.
 *
 * Field names are camelCase because the hook runs responses
 * through `snakeCaseToCamelCase` before storing them in state.
 *
 * Target path: definitions/portal/programReviewTool/JobRun.types.ts
 */

/** Mirrors the JobStatus enum from the Django model. */
export type JobStatus = "running" | "success" | "failure";

/** Shape of a single record returned by GET /v1/program-review-tool/job-run */
export interface IJobRun {
  id: number;
  jobName: string;
  status: JobStatus;
  user: string | null;
  startedAt: string;
  finishedAt: string | null;
  duration: number | null;
  errorMsg: string | null;
  created: string;
  modified: string;
}

/** Shape of a single record returned by GET /v1/program-review-tool/job-run/registry */
export interface IRegistryJob {
  jobName: string;
  functionName: string;
}
