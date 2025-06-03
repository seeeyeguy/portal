import lodash from "lodash";
import { toast } from "react-toastify";

import portfolioApi from "state/query/api/portal/programReviewTool/PortfolioApi";
import programApi from "state/query/api/portal/programReviewTool/ProgramApi";

import {
  IProgramReviewToolSlice,
  initialState,
  loadProgramReview,
  updateCurrentPortfolio,
} from "state/slices/ProgramReviewToolSlice";
import { AppDispatch } from "state/store/store";

import {
  IPortfolio,
  IPortfolios,
} from "views/definitions/ProgramReviewTool.types";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";

/**
 * Loads initial state for Program Review Tool.
 *
 * @param {string} user user to load portfolios for.
 */
export const loadProgramReviewState =
  (user: string) => async (dispatch: AppDispatch) => {
    // Load inital programs
    const promisePrograms = dispatch(
      programApi.endpoints.getPrograms.initiate([])
    );
    // Load inital user portfolios
    const promisePortfolios = dispatch(
      portfolioApi.endpoints.getPortfolios.initiate(user)
    );

    const [programsResponse, portfoliosResponse] = await Promise.all([
      promisePrograms,
      promisePortfolios,
    ]);

    const {
      error: programsError,
      isSuccess: isProgramsSuccess,
      isError: isProgramsError,
    } = programsResponse;

    const {
      data: portfoliosData,
      error: portfoliosError,
      isSuccess: isPortfoliosSuccess,
      isError: isPortfoliosError,
    } = portfoliosResponse;

    if (isProgramsError && programsError) {
      const message =
        "data" in programsError
          ? (programsError.data as string)
          : DEFAULT_API_ERROR_MESSAGE;

      console.error(programsError);
      toast.error(`Error: ${message}`);
    }

    if (isPortfoliosError && portfoliosError) {
      const message =
        "data" in portfoliosError
          ? (portfoliosError.data as string)
          : DEFAULT_API_ERROR_MESSAGE;

      console.error(portfoliosError);
      toast.error(`Error: ${message}`);
    }

    if (isProgramsSuccess && isPortfoliosSuccess) {
      const retrievedPortfolios =
        portfoliosData?.data as unknown as IPortfolios;

      const newSlice = {
        currentPortfolio: initialState.currentPortfolio,
      } as IProgramReviewToolSlice;

      if (!lodash.isEmpty(retrievedPortfolios)) {
        // Select the latest portfolio on load.
        const usersPortfolios = Object.values(retrievedPortfolios);
        const latestPortfolio = usersPortfolios.reduce(
          (latest, portfolio) =>
            new Date(portfolio.modified) > new Date(latest.modified)
              ? portfolio
              : latest,
          usersPortfolios[0]
        );

        // Copy latest portfolio so it can be modified without affecting original.
        newSlice.currentPortfolio = {
          ...retrievedPortfolios[latestPortfolio.id],
        };
      }

      dispatch(loadProgramReview(newSlice));
    }
  };

/**
 * Deletes a user portfolio.
 *
 * @param {number} portfolioId Id of portfolio to delete.
 */
export const deletePortfolioState =
  (portfolioId: number) => async (dispatch: AppDispatch) => {
    const promiseRemovePortfolio = dispatch(
      portfolioApi.endpoints.removePortfolio.initiate(portfolioId)
    );

    const { error } = await promiseRemovePortfolio;

    if (error) {
      console.error(error);
      toast.error(`Error: Failed to delete portfolio.`);
    }
  };

/**
 * Update user portfolio.
 *
 * @param {number} portfolioId Id of portfolio to update.
 * @param {string} name New name of portfolio.
 * @param {number[]} programs Ids of the programs that will be in the portfolio.
 */
export const editPortfolioState =
  (id: number, name: string, programs: number[]) =>
  async (dispatch: AppDispatch) => {
    const promisePortfolios = dispatch(
      portfolioApi.endpoints.updatePortfolio.initiate({
        id,
        name,
        programs,
      })
    );
    const { data: portfoliosResponse, error } = await promisePortfolios;
    const retreivedPortfolio =
      portfoliosResponse?.data as unknown as IPortfolio;

    if (error) {
      console.error(error);
      toast.error(`Error: Failed to update portfolio.`);
    }

    if (retreivedPortfolio?.id) {
      dispatch(updateCurrentPortfolioState(retreivedPortfolio));
    }
  };

/**
 * Add a new user portfolio.
 *
 * @param {string} name Name of the new portfolio.
 * @param {number[]} programs Ids of the programs that will be in the portfolio.
 */
export const addPortfolioState =
  (name: string, programs: number[]) => async (dispatch: AppDispatch) => {
    const promisePortfolios = dispatch(
      portfolioApi.endpoints.addPortfolio.initiate({
        name,
        programs,
      })
    );
    const { data: portfoliosResponse, error } = await promisePortfolios;
    const retreivedPortfolio =
      portfoliosResponse?.data as unknown as IPortfolio;

    if (error) {
      console.error(error);
      toast.error(`Error: Failed to save portfolio.`);
    }

    if (retreivedPortfolio?.id) {
      dispatch(updateCurrentPortfolioState(retreivedPortfolio));
    }
  };

/**
 * Update the data of the currently viewed portfolio.
 *
 * @param {IPortfolio | null} portfolio New portfolio data.
 */
export const updateCurrentPortfolioState =
  (portfolio: IPortfolio | null) => async (dispatch: AppDispatch) => {
    dispatch(updateCurrentPortfolio(portfolio));
  };

/**
 * Select the most recent portfolio to show as the currently viewed portolio.
 *
 * @param {IPortfolios} portfolios Portfolios to choose from.
 * @param {number} excludedPortfolio Portfolio id to be excluded when choosing the next portfolio.
 */
export const setNextPortfolioState =
  (portfolios: IPortfolios, excludedPortfolio: number) =>
  async (dispatch: AppDispatch) => {
    let newCurrentPortfolio = initialState.currentPortfolio;

    if (!lodash.isEmpty(portfolios)) {
      const latestPortfolio = Object.values(portfolios).reduce(
        (latest, portfolio) => {
          if (portfolio.id === excludedPortfolio) {
            return latest;
          }
          if (
            !latest ||
            new Date(portfolio.modified) > new Date(latest.modified)
          ) {
            return portfolio;
          }
          return latest;
        },
        null as IPortfolio | null
      );

      if (latestPortfolio) {
        // Copy latest portfolio so it can be modified without affecting original.
        newCurrentPortfolio = { ...portfolios[latestPortfolio.id] };
      }
    }

    dispatch(updateCurrentPortfolio(newCurrentPortfolio));
  };
