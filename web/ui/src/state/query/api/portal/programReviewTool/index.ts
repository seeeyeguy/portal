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

export default {
  portfolioApi,
  programApi,
  useAddPortfolioMutation,
  useGetPortfoliosQuery,
  useUpdatePortfolioMutation,
  useRemovePortfolioMutation,
  useGetProgramsQuery,
  useGetProgramsReviewMutation,
};
