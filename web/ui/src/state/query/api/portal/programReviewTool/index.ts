import portfolioApi, {
  useAddPortfolioMutation,
  useGetPortfoliosQuery,
  useUpdatePortfolioMutation,
  useRemovePortfolioMutation,
} from "state/query/api/portal/programReviewTool/PortfolioApi";
import programApi, {
  useGetProgramsQuery,
  useGetProgramsReviewMutation,
} from "state/query/api/portal/programReviewTool/ProgramApi";
import recordApi, {
  useAddRecordMutation,
  useGetRecordQuery,
  useGetReportingPeriodQuery,
} from "state/query/api/portal/programReviewTool/RecordApi";

export default {
  portfolioApi,
  programApi,
  recordApi,
  useAddPortfolioMutation,
  useGetPortfoliosQuery,
  useUpdatePortfolioMutation,
  useRemovePortfolioMutation,
  useGetProgramsQuery,
  useGetProgramsReviewMutation,
  useAddRecordMutation,
  useGetRecordQuery,
  useGetReportingPeriodQuery,
};
