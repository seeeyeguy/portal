import saveAs from "file-saver";
import lodash from "lodash";

import { POST, GET } from "definitions/RequestConstants";
import { CREATED, OK } from "definitions/StatusCodeConstants";
import endpoints from "services/api";
import api from "state/query/api";
import {
  IApiProgram,
  transformProgramRecord,
} from "state/query/api/portal/programReviewTool/ProgramHelper";

import {
  EReviewStatus,
  IPrograms,
} from "views/definitions/ProgramReviewTool.types";

type TApiProgramResponse = {
  data: IPrograms;
  status: number | undefined;
};

export type TApiFetchProgramRequest = {
  ids?: number[];
  paNumbers?: string[];
  programMember?: string;
  tiers?: number[];
  activeOnly?: boolean;
  page?: number;
  limit?: number;
};

export type TApiProgramReviewRequest = {
  programs: number[];
  name: string;
};

export type TApiProgramReviewErrorResponse = {
  data: string;
  status: number;
};

type TApiProgramReviewResponse = {
  data: number;
  status: number | undefined;
};

const programApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getPrograms: builder.query<TApiProgramResponse, TApiFetchProgramRequest>({
      query: ({
        ids = null,
        paNumbers = null,
        programMember = null,
        tiers = null,
        activeOnly = null,
        page = null,
        limit = null,
      }) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PROGRAM(
          ids,
          paNumbers,
          programMember,
          tiers,
          activeOnly,
          page,
          limit
        ),
        method: GET,
      }),
      transformResponse: (
        response: IApiProgram | IApiProgram[],
        meta
      ): TApiProgramResponse => ({
        data: lodash.isArray(response)
          ? response.reduce(
              (acc, program) => ({
                ...acc,
                [program.pa_number.toUpperCase()]: transformProgramRecord(program),
              }),
              {}
            )
          : transformProgramRecord(response),
        status: meta?.response?.status,
      }),
    }),
    getProgramsReview: builder.mutation<
      TApiProgramReviewResponse,
      TApiProgramReviewRequest
    >({
      query: (body: TApiProgramReviewRequest) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PROGRAM_REVIEW,
        method: POST,
        body,
        responseHandler: (response) =>
          response.headers.get("Content-Type")?.includes("application/json")
            ? response.json()
            : response.blob(),
      }),
      transformResponse: (
        response: string | Blob,
        meta
      ): TApiProgramReviewResponse => {
        const responseStatusCode = meta?.response?.status;

        if (responseStatusCode !== OK && responseStatusCode !== CREATED) {
          return {
            data: EReviewStatus.ERROR,
            status: responseStatusCode,
          };
        }

        // Check if response is a portfolio query status (int).
        const responseStatus = parseInt(response as string);
        if (lodash.isNumber(responseStatus) && responseStatusCode === OK) {
          return {
            data: responseStatus,
            status: responseStatusCode,
          };
        }

        // Download file.
        const contentDisposition = meta?.response?.headers.get(
          "Content-Disposition"
        );
        const fileName = contentDisposition?.match(/filename=([^;]+)/)?.[1];
        saveAs(response, fileName);
        return {
          data: EReviewStatus.COMPLETE,
          status: responseStatusCode,
        };
      },
    }),
  }),
});

export default programApi;
export const { useGetProgramsQuery, useGetProgramsReviewMutation } = programApi;
