import { createSlice, PayloadAction } from "@reduxjs/toolkit";

import {
  DEFAULT_PORTFOLIO_ID,
  IPortfolio,
} from "views/definitions/ProgramReviewTool.types";

/** Interface for program review slice. */
export interface IProgramReviewToolSlice {
  /** Portfolio of programs of that represent the users currently displayed data. */
  currentPortfolio: IPortfolio;
}

export const initialState: IProgramReviewToolSlice = {
  currentPortfolio: {
    id: DEFAULT_PORTFOLIO_ID,
    programs: {},
    name: "",
    created: new Date().toISOString(),
    modified: new Date().toISOString(),
  },
};

const ProgramReviewToolSlice = createSlice({
  name: "programReviewTool",
  initialState,
  reducers: {
    clearProgramReviewToolState: () => ({
      ...initialState,
    }),
    clearCurrentPortfolio: (state) => ({
      ...state,
      currentPortfolio: initialState.currentPortfolio,
    }),
    loadProgramReview: (_, action: PayloadAction<IProgramReviewToolSlice>) => ({
      ...action.payload,
    }),
    updateCurrentPortfolio: (
      state,
      action: PayloadAction<IPortfolio | null | undefined>
    ) => ({
      ...state,
      currentPortfolio: action.payload ?? initialState.currentPortfolio,
    }),
  },
});

export const {
  clearCurrentPortfolio,
  clearProgramReviewToolState,
  loadProgramReview,
  updateCurrentPortfolio,
} = ProgramReviewToolSlice.actions;
export default ProgramReviewToolSlice.reducer;
