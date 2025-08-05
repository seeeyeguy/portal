import React from "react";
import { useLoaderData } from "react-router";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import lodash from "lodash";

import FAQModal from "views/components/FAQModal/FAQModal";
import NavBar from "views/components/NavBar/NavBar";
import PortfolioMenu from "views/containers/PortfolioMenu/PortfolioMenu";
import ProgramList from "views/containers/ProgramList/ProgramList";

import { IProfile } from "definitions/portal/users/Profile.types";
import type { IAuthUser } from "definitions/Sso.types";
import { IProgressMarker } from "views/components/ProgressBar/ProgressBar";
import {
  DEFAULT_PORTFOLIO_ID,
  EReviewStatus,
  IPortfolio,
  IPortfolios,
} from "views/definitions/ProgramReviewTool.types";

import {
  addPortfolioState,
  deletePortfolioState,
  editPortfolioState,
  loadProgramReviewState,
  setNextPortfolioState,
  updateCurrentPortfolioState,
} from "state/actions/ProgramReviewActions";
import { useGetPortfoliosQuery } from "state/query/api/portal/programReviewTool/PortfolioApi";
import programApi from "state/query/api/portal/programReviewTool/ProgramApi";
import { useGetProfileUserQuery } from "state/query/api/portal/users/UsersApi";
import store, { useAppDispatch, useTypedSelector } from "state/store/store";

import useInterval from "views/utils/IntervalUtility";

import styles from "views/pages/ProgramReviewTool/ProgramReviewTool.module.css";

const DEFAULT_LABELS = { completeLabel: "", incompleteLabel: "" };
const GENERATE_REVIEW_PROGRESS_MARKERS = [
  {
    id: EReviewStatus.SUBMITTED,
    name: "Submitted",
    complete: true,
    ...DEFAULT_LABELS,
  },
  {
    id: EReviewStatus.QUEUED,
    name: "Gathering Info",
    complete: false,
    ...DEFAULT_LABELS,
  },
  {
    id: EReviewStatus.PROCESSING,
    name: "Creating Review",
    complete: false,
    ...DEFAULT_LABELS,
  },
  {
    id: EReviewStatus.COMPLETE,
    name: "Complete",
    complete: false,
    ...DEFAULT_LABELS,
  },
];
const PORTFOLIO_POLL_INTERVAL = 10000;
const PORTFOLIO_POLL_MAX_REQUESTS = 18;

export default function ProgramReviewTool() {
  const loaderData = useLoaderData() as { user: IAuthUser };

  // Refs to manipulate navbar profile menu.
  const smNavBarRef = React.useRef<HTMLElement>(null);
  const mdNavBarRef = React.useRef<HTMLElement>(null);
  const lgNavBarRef = React.useRef<HTMLElement>(null);

  const [polling, setPolling] = React.useState<number>(0);
  const [currentMarker, setCurrentMarker] = React.useState<number | null>(null);
  const [progressMarkers, setProgressMarkers] = React.useState<
    IProgressMarker[]
  >([]);

  const dispatch = useAppDispatch();

  const { data: profileApiResponse } = useGetProfileUserQuery(
    loaderData.user.email
  );

  const profile = (profileApiResponse?.data ?? {
    user: {
      firstName: loaderData.user.firstName,
      lastName: loaderData.user.lastName,
      email: loaderData.user.email,
    },
    jobTitle: "UNKNOWN",
    citizenship: "UNKNOWN",
  }) as IProfile;

  // Load initial user portfolios and program review state data.
  React.useEffect(() => {
    dispatch(loadProgramReviewState(loaderData.user.email));
  }, [loaderData, dispatch]);

  const { data: portfoliosResponse, isLoading } = useGetPortfoliosQuery(
    loaderData.user.email
  );

  const portfolios = portfoliosResponse?.data as IPortfolios;

  const currentPortfolio = useTypedSelector(
    (state) => state.ProgramReviewTool.currentPortfolio
  );

  // Portfolio Review request properties.
  const [reviewName, setReviewName] = React.useState<string>();
  const [reviewPrograms, setReviewPrograms] = React.useState<number[]>([]);

  const closeNavBarProfile = React.useCallback(() => {
    if (smNavBarRef.current) {
      smNavBarRef.current.click();
    }
    if (mdNavBarRef.current) {
      mdNavBarRef.current.click();
    }
    if (lgNavBarRef.current) {
      lgNavBarRef.current.click();
    }
  }, []);

  const getPortfolioStatus = React.useCallback(
    async (programs: number[], name: string) => {
      const ProgramReviewResponse = await store.dispatch(
        programApi.endpoints.getProgramsReview.initiate({
          programs: programs,
          name: name,
        })
      );

      // Portfolio generation is complete.
      if (ProgramReviewResponse.data?.data === EReviewStatus.COMPLETE) {
        setPolling(0);
        setProgressMarkers([]);
        setCurrentMarker(null);
        toast.success("Portfolio Generation Complete.");
        return;
      }

      // There is an error.
      if (
        !lodash.isNumber(ProgramReviewResponse.data?.data) ||
        ProgramReviewResponse.data?.data === EReviewStatus.ERROR ||
        ProgramReviewResponse.error
      ) {
        setPolling(0);
        setProgressMarkers([]);
        setCurrentMarker(null);
        toast.error(`Error: Portfolio generation failed.`);
        return;
      }

      // Polling time out.
      if (polling > PORTFOLIO_POLL_MAX_REQUESTS) {
        setPolling(0);
        setProgressMarkers([]);
        setCurrentMarker(null);
        toast.error(`Portfolio generation timed out.`);
        return;
      }

      // Update previous progress markers to be complete.
      const newStatus = ProgramReviewResponse.data.data;
      setProgressMarkers((prevMarkers) =>
        prevMarkers.map((marker) =>
          marker.id <= newStatus ? { ...marker, complete: true } : marker
        )
      );

      setCurrentMarker(newStatus);
      setPolling((prevCount) => prevCount + 1);
    },
    [polling, setProgressMarkers, setCurrentMarker]
  );

  // Poll progress of portfolio generation.
  useInterval(() => {
    if (currentMarker !== null && reviewName && reviewPrograms) {
      getPortfolioStatus(reviewPrograms, reviewName);
    }
  }, polling && PORTFOLIO_POLL_INTERVAL);

  const handleGeneratePortfolio = React.useCallback(async () => {
    if (!lodash.isEmpty(currentPortfolio.programs)) {
      const validPrograms = Object.values(currentPortfolio.programs)
        .filter((program) => program.activeStatus && !program.disabled)
        .map((program) => program.id);

      let createdReviewName = currentPortfolio.name;

      // If the portfolio has not been saved.
      if (currentPortfolio.id === DEFAULT_PORTFOLIO_ID) {
        // If there is only one program, name the unsaved portfolio after the program.
        if (validPrograms.length === 1) {
          createdReviewName =
            Object.values(currentPortfolio.programs).find(
              (program) => program.id === validPrograms[0]
            )?.name ?? "Custom Portfolio";
        } else {
          // Multiple programs in unsaved portfolio.
          createdReviewName = "Custom Portfolio";
        }
      }

      setPolling(1);
      setProgressMarkers(GENERATE_REVIEW_PROGRESS_MARKERS);
      setCurrentMarker(EReviewStatus.SUBMITTED);
      setReviewName(createdReviewName);
      setReviewPrograms(validPrograms);
      getPortfolioStatus(validPrograms, createdReviewName);
    }
  }, [currentPortfolio, getPortfolioStatus]);

  const handleSavePortfolio = React.useCallback(
    (name: string, newPortfolio: IPortfolio) => {
      if (lodash.isEmpty(newPortfolio.programs)) {
        return;
      }

      const portfolioPAs = Object.values(newPortfolio.programs).map(
        (program) => program.id
      );

      if (newPortfolio.id === DEFAULT_PORTFOLIO_ID) {
        dispatch(addPortfolioState(name, portfolioPAs));
      } else {
        dispatch(editPortfolioState(newPortfolio.id, name, portfolioPAs));
      }
    },
    [dispatch]
  );

  const handleDeletePortfolio = React.useCallback(
    (portfolioId: number) => {
      if (currentPortfolio.id === portfolioId) {
        dispatch(setNextPortfolioState(portfolios, portfolioId));
      }
      dispatch(deletePortfolioState(portfolioId));
    },
    [currentPortfolio, portfolios, dispatch]
  );

  if (!loaderData.user.email) {
    return <div>:x: 404</div>;
  }

  return (
    <div
      id="app-container"
      onClick={() => {
        closeNavBarProfile();
      }}
      aria-description="container for program review tool application"
    >
      <FAQModal />
      <NavBar
        profile={profile}
        hideSearchBar={true}
        navBarRefs={[smNavBarRef, mdNavBarRef, lgNavBarRef]}
      />

      <div id="page-content">
        <header className={styles["program-review-header"]}>
          <h1>Program Review Tool</h1>
        </header>
        <div
          className={styles["program-review-container"]}
          aria-description="container for program review content"
        >
          {isLoading ? (
            <div
              className={styles["program-review-loading"]}
              aria-description="container to display when loading data"
            >
              <MoonLoader />
            </div>
          ) : (
            <ProgramList
              portfolio={currentPortfolio}
              setPortfolioPrograms={(updatedPrograms) =>
                dispatch(
                  updateCurrentPortfolioState({
                    ...currentPortfolio,
                    programs: { ...updatedPrograms },
                  })
                )
              }
            />
          )}

          <PortfolioMenu
            portfolios={portfolios}
            selectedPortfolio={currentPortfolio}
            loading={isLoading}
            progressMarkers={progressMarkers}
            currentMarker={
              lodash.isNumber(currentMarker) ? currentMarker : null
            }
            deletePortfolio={(id) => handleDeletePortfolio(id)}
            generatePortfolio={() => handleGeneratePortfolio()}
            savePortfolio={(name: string) =>
              handleSavePortfolio(name, currentPortfolio)
            }
            setPortfolio={(id) =>
              dispatch(updateCurrentPortfolioState(id ? portfolios[id] : null))
            }
          />
        </div>
      </div>
    </div>
  );
}
