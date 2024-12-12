import React from "react";
import { useLoaderData } from "react-router";
import { toast } from "react-toastify";
import { LoadingButton } from "adas-react-components";
import lodash from "lodash";

import { SaveSessionButtonProps } from "components/buttons/SaveSessionButton/types";

import queryFilterStateApi, {
  useGetQueryFilterStateQuery,
  ApiQueryFilterStateMutationRequest,
} from "state/query/api/portal/preferences/QueryFilterState";
import { useAppDispatch, useTypedSelector } from "state/store";

import { User } from "state/types/services/sso";

import { DEFAULT_API_ERROR_MESSAGE } from "utils/constants/errors";
import { delay } from "utils/promises";

const DELAY = 500;

export default function SaveSessionButton({
  filterData,
  filterTags,
  className,
}: SaveSessionButtonProps) {
  const loaderData = useLoaderData() as { user: User };

  const dispatch = useAppDispatch();

  const searchParams = useTypedSelector((state) => state.ResourceSearch);

  const { data: queryFilterStateApiResponse } = useGetQueryFilterStateQuery(
    loaderData.user.email
  );
  const queryFilterStateId = queryFilterStateApiResponse?.data.id;

  const [state, setState] = React.useState({
    isLoading: false,
    isSuccess: false,
    isError: false,
  });

  const { isLoading, isSuccess, isError } = state;

  const filterDataValues = React.useMemo(
    () =>
      lodash
        .values(filterData.current)
        .reduce((acc, filters) => [...acc, ...filters], []),
    [filterData]
  );

  const saveSessionData = React.useCallback(async () => {
    setState({
      isLoading: true,
      isSuccess: false,
      isError: false,
    });

    const body: ApiQueryFilterStateMutationRequest = {
      ...searchParams,
      search: searchParams.search.record,
      tags: filterTags
        .filter((record) => {
          const filterLabel = record.label.slice(8);
          const [, filterValue] = filterLabel.split(":");
          return filterDataValues.includes(filterValue);
        })
        .map((record) => record.id),
    };
    const promise = dispatch(
      queryFilterStateApi.endpoints.postQueryFilterState.initiate({
        body,
        post: !queryFilterStateId,
        id: queryFilterStateId,
      })
    );
    const { data, error } = await promise;
    const isSuccess = !!data;
    const isError = !!error;

    await delay(DELAY);

    if (isSuccess) {
      localStorage.setItem("filterData", JSON.stringify(filterData.current));
      setState({
        isLoading: false,
        isSuccess: isSuccess,
        isError: false,
      });
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
  }, [
    filterData,
    filterDataValues,
    filterTags,
    queryFilterStateId,
    searchParams,
    dispatch,
    setState,
  ]);

  return (
    <LoadingButton
      label="Save Session"
      loadingText="Saving Session..."
      successText="Session Saved!"
      errorText="Session Not Saved!"
      isLoading={isLoading}
      isSuccess={isSuccess}
      isError={isError}
      width={12.5}
      height={3.5}
      spinner="moon"
      disabled={isLoading}
      className={className}
      onClick={saveSessionData}
    />
  );
}
