import React from "react";
import { useLoaderData } from "react-router";
import { toast } from "react-toastify";
import { LoadingButton } from "adas-react-components";

import { LoadSessionButtonProps } from "components/buttons/LoadSessionButton/types";

import queryFilterStateApi from "state/query/api/portal/preferences/QueryFilterState";
import { loadDirectoryResourceSearch } from "state/slices/portal/directory/Resource/Search";
import { useAppDispatch } from "state/store";

import { SearchParams } from "state/types/portal/directory/Resource/Search";
import { User } from "state/types/services/sso";

import { DEFAULT_API_ERROR_MESSAGE } from "utils/constants/errors";
import { delay } from "utils/promises";

const DELAY = 500;

export default function LoadSessionButton({
  filterData,
  className,
}: LoadSessionButtonProps) {
  const loaderData = useLoaderData() as { user: User };

  const dispatch = useAppDispatch();

  const [state, setState] = React.useState({
    isLoading: false,
    isSuccess: false,
    isError: false,
  });

  const { isLoading, isSuccess, isError } = state;

  const loadSessionData = React.useCallback(async () => {
    setState({
      isLoading: true,
      isSuccess: false,
      isError: false,
    });

    const promise = dispatch(
      queryFilterStateApi.endpoints.getQueryFilterState.initiate(
        loaderData.user.email
      )
    );
    const { data: response, error, isSuccess, isError } = await promise;

    await delay(DELAY);

    const payload: SearchParams = {
      search: {
        term: response?.data.search?.searchTerm ?? "",
        record: response?.data.search?.id ?? null,
      },
      functions: response?.data.functions ?? [],
      employeeLevels: response?.data.employeeLevels ?? [],
      tags: response?.data.tags ?? [],
    };

    if (isSuccess) {
      filterData.current = JSON.parse(
        localStorage.getItem("filterData") ?? "{}"
      );
      setState({
        isLoading: false,
        isSuccess: isSuccess,
        isError: false,
      });
      dispatch(loadDirectoryResourceSearch(payload));
    }

    if (isError) {
      setState({
        isLoading: false,
        isSuccess: false,
        isError: isError,
      });
      if (error) {
        const message =
          "data" in error ? (error.data as string) : DEFAULT_API_ERROR_MESSAGE;
        toast.error(message);
      }
    }

    await delay(DELAY);

    setState({
      isLoading: false,
      isSuccess: false,
      isError: false,
    });
  }, [filterData, loaderData, dispatch, setState]);

  return (
    <LoadingButton
      label="Load Session"
      loadingText="Loading Session..."
      successText="Session Loaded!"
      errorText="Session Not Loaded!"
      isLoading={isLoading}
      isSuccess={isSuccess}
      isError={isError}
      width={12.5}
      height={3.5}
      spinner="moon"
      disabled={isLoading}
      className={className}
      onClick={loadSessionData}
    />
  );
}
