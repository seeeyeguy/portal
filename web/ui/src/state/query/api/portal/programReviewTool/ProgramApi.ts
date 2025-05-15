import lodash from "lodash";

import endpoints from "services/api";
import { POST, GET } from "definitions/RequestConstants";
import {
  ApiProgram,
  transformProgramRecord,
} from "utils/portal/programReviewTool/ProgramTransformUtility";
import api from "state/query/api";

import Program from "state/types/program_review_tool/Program";

type ApiProgramResponse = {
  data: { [key: string]: Program };
  status: number | undefined;
};

type ApiProgramReviewRequest = {
  programs: number[];
  review_name: string;
};

const programApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getPrograms: builder.query<ApiProgramResponse, number[]>({
      query: (ids: number[]) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PROGRAM(ids),
        method: GET,
      }),
      transformResponse: (
        response: ApiProgram | ApiProgram[],
        meta
      ): ApiProgramResponse => ({
        data: lodash.isArray(response)
          ? response.reduce(
              (acc, program) => ({
                ...acc,
                [program.pa_number]: transformProgramRecord(program),
              }),
              {}
            )
          : transformProgramRecord(response),
        status: meta?.response?.status,
      }),
    }),
    getProgramsReview: builder.mutation<number, ApiProgramReviewRequest>({
      query: (body: ApiProgramReviewRequest) => ({
        url: endpoints.PORTAL.PROGRAM_REVIEW_TOOL.PROGRAM_REVIEW,
        method: POST,
        body,
      }),
    }),
  }),
});

export default programApi;
export const { useGetProgramsQuery, useGetProgramsReviewMutation } = programApi;
