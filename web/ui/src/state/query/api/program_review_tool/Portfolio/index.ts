import endpoints from "routes/api/endpoints";
import { POST, GET, PUT, DELETE } from "routes/api/helpers/headers/init";
import {
  ApiPortfolio,
  transformPortfolioRecord,
} from "routes/api/helpers/transforms/portal/response/program_review_tool/Portfolio";
import { transformProgramRecord } from "routes/api/helpers/transforms/portal/response/program_review_tool/Program";
import api from "state/query/api";

import Portfolio from "state/types/program_review_tool/Portfolio";
import Program from "state/types/program_review_tool/Program";

interface IndexedPortfolio extends Omit<Portfolio, "programs"> {
  programs: { [key: string]: Program };
}

type ApiPortfolioResponse = {
  data: { [key: number]: IndexedPortfolio } | Portfolio;
  status: number | undefined;
};

type ApiPortfolioRequest = {
  name: string;
  programs: number[];
};

const portfolioApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addPortfolio: builder.mutation<ApiPortfolioResponse, ApiPortfolioRequest>({
      query: (body) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PORTFOLIO(),
        method: POST,
        body,
      }),
      transformResponse: (response: ApiPortfolio, meta) => ({
        data: transformPortfolioRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Portfolio"],
    }),
    getPortfolios: builder.query<ApiPortfolioResponse, string>({
      query: (user: string) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PORTFOLIO(user),
        method: GET,
      }),
      transformResponse: (
        response: ApiPortfolio[],
        meta
      ): ApiPortfolioResponse => ({
        data: response?.reduce((acc, portfolio) => {
          const indexedPrograms =
            portfolio?.programs?.reduce(
              (acc, program) => ({
                ...acc,
                [program.pa_number]: transformProgramRecord(program),
              }),
              {}
            ) ?? {};
          return {
            ...acc,
            [portfolio.id]: {
              ...transformPortfolioRecord(portfolio),
              programs: indexedPrograms,
            },
          };
        }, {}),
        status: meta?.response?.status,
      }),
    }),
    updatePortfolio: builder.mutation<
      ApiPortfolioResponse,
      { id: number } & ApiPortfolioRequest
    >({
      query: ({ id, name, programs }) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PORTFOLIO(id),
        method: PUT,
        body: {
          name,
          programs,
        },
      }),
      transformResponse: (response: ApiPortfolio, meta) => ({
        data: transformPortfolioRecord(response),
        status: meta?.response?.status,
      }),
      invalidatesTags: ["Portfolio"],
    }),
    removePortfolio: builder.mutation<number, number>({
      query: (id: number) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PORTFOLIO(id),
        method: DELETE,
      }),
      invalidatesTags: ["Portfolio"],
    }),
  }),
});

export default portfolioApi;
export const {
  useAddPortfolioMutation,
  useGetPortfoliosQuery,
  useUpdatePortfolioMutation,
  useRemovePortfolioMutation,
} = portfolioApi;
