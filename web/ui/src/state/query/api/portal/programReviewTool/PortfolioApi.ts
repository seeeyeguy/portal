import { POST, GET, PUT, DELETE } from "definitions/RequestConstants";
import endpoints from "services/api";
import api from "state/query/api";
import {
  IApiPortfolio,
  transformPortfolioRecord,
} from "state/query/api/portal/programReviewTool/PortfolioHelper";
import { transformProgramRecord } from "state/query/api/portal/programReviewTool/ProgramHelper";

import {
  IPortfolio,
  IPortfolios,
} from "views/definitions/ProgramReviewTool.types";

type TApiPortfolioResponse = {
  data: IPortfolios | IPortfolio;
  status: number | undefined;
};

type TApiPortfolioRequest = {
  name: string;
  programs: number[];
};

const portfolioApi = api.injectEndpoints({
  endpoints: (builder) => ({
    addPortfolio: builder.mutation<TApiPortfolioResponse, TApiPortfolioRequest>(
      {
        query: (body: TApiPortfolioRequest) => ({
          url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PORTFOLIO(),
          method: POST,
          body,
        }),
        transformResponse: (response: IApiPortfolio, meta) => {
          const indexedPrograms =
            response?.programs?.reduce(
              (acc, program) => ({
                ...acc,
                [program.pa_number]: transformProgramRecord(program),
              }),
              {}
            ) ?? {};
          return {
            data: {
              ...transformPortfolioRecord(response),
              programs: indexedPrograms,
            },
            status: meta?.response?.status,
          };
        },
        invalidatesTags: ["Portfolio"],
      }
    ),
    getPortfolios: builder.query<TApiPortfolioResponse, string>({
      query: (user: string) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PORTFOLIO(user),
        method: GET,
      }),
      transformResponse: (
        response: IApiPortfolio[],
        meta
      ): TApiPortfolioResponse => ({
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
      providesTags: ["Portfolio"],
    }),
    updatePortfolio: builder.mutation<
      TApiPortfolioResponse,
      { id: number } & TApiPortfolioRequest
    >({
      query: ({
        id,
        name,
        programs,
      }: { id: number } & TApiPortfolioRequest) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PORTFOLIO(id),
        method: PUT,
        body: {
          name,
          programs,
        },
      }),
      transformResponse: (response: IApiPortfolio, meta) => {
        const indexedPrograms =
          response?.programs?.reduce(
            (acc, program) => ({
              ...acc,
              [program.pa_number]: transformProgramRecord(program),
            }),
            {}
          ) ?? {};
        return {
          data: {
            ...transformPortfolioRecord(response),
            programs: indexedPrograms,
          },
          status: meta?.response?.status,
        };
      },
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
