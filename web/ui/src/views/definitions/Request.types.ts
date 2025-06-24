export enum ERequestStage {
  DRAFT = 1, // Draft.
  SUBMITTED = 2, // Submitted.
  APPROVED_BUSINESS_PROCESS_EXPERT = 3, // Approved by Business Process Expert.
  REVISE = 4, // Revise.
  REJECTED_BUSINESS_PROCESS_EXPERT = 5, // Rejected by Business Process Expert.
  APPROVED_SUPERUSER = 6, // Approved by Superuser.
  REJECTED_SUPERUSER = 7, // Rejected by Superuser.
}
