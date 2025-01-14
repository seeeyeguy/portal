import lodash from "lodash";

import queryFilterStateApi, {
  ApiQueryFilterStateMutationRequest,
} from "state/query/api/portal/preferences/QueryFilterState";
import {
  loadDirectoryResourceSearch,
  toggleEmployeeLevels,
  toggleFunctions,
  toggleTags,
  updateSearchRecord,
  updateSearchTerm,
} from "state/slices/portal/directory/Resource/Search";
import { AppDispatch } from "state/store";

import Query from "state/types/portal/analytics/Query";
import { SearchParams } from "state/types/portal/directory/Resource/Search";
import Tag from "state/types/portal/directory/Tag";

import { DEFAULT_API_ERROR_MESSAGE } from "utils/constants/errors";

export const loadDirectoryResourceSearchState =
  (user: string) => async (dispatch: AppDispatch) => {
    const promise = dispatch(
      queryFilterStateApi.endpoints.getQueryFilterState.initiate(user)
    );
    const { data: response, error, isSuccess, isError } = await promise;
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
      dispatch(loadDirectoryResourceSearch(payload));
    }
    if (isError && error) {
      const message =
        "data" in error ? (error.data as string) : DEFAULT_API_ERROR_MESSAGE;
      console.error(message);
    }
  };

export const toggleEmployeeLevel =
  (
    functions: number[],
    employees: number[],
    filterTags: Tag[],
    filterData: React.MutableRefObject<{ [key: string]: string[] }>,
    filterDataValues: string[],
    queryFilterStateId: number | null = null
  ) =>
  (id: number) =>
  async (dispatch: AppDispatch) => {
    if (!lodash.isInteger(id)) {
      return;
    }

    dispatch(toggleEmployeeLevels(id));

    const body: ApiQueryFilterStateMutationRequest = {
      functions: functions,
      employeeLevels: lodash.xor(employees, [id]),
      search: null,
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

    const { data } = await promise;
    const isSuccess = !!data;

    if (isSuccess) {
      localStorage.setItem("filterData", JSON.stringify(filterData.current));
    }
  };

export const toggleFunction =
  (
    functions: number[],
    employees: number[],
    filterTags: Tag[],
    filterData: React.MutableRefObject<{ [key: string]: string[] }>,
    filterDataValues: string[],
    queryFilterStateId: number | null = null
  ) =>
  (id: number) =>
  async (dispatch: AppDispatch) => {
    if (!lodash.isInteger(id)) {
      return;
    }

    dispatch(toggleFunctions(id));

    const body: ApiQueryFilterStateMutationRequest = {
      functions: lodash.xor(functions, [id]),
      employeeLevels: employees,
      search: null,
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

    const { data } = await promise;
    const isSuccess = !!data;

    if (isSuccess) {
      localStorage.setItem("filterData", JSON.stringify(filterData.current));
    }
  };

export const toggleTag = (id: number) => (dispatch: AppDispatch) => {
  if (!lodash.isInteger(id)) {
    return;
  }
  dispatch(toggleTags(id));
};

export const updateSearchStateRecord =
  (record: Query) => (dispatch: AppDispatch) => {
    const queryRecordFields = [
      "id",
      "user",
      "searchTerm",
      "resources",
      "created",
    ];
    const isQueryRecord =
      lodash.difference(lodash.keys(record), queryRecordFields).length === 0;

    if (!(lodash.isPlainObject(record) && isQueryRecord)) {
      return;
    }

    if (!lodash.isInteger(record.id)) {
      return;
    }

    dispatch(updateSearchRecord(record.id));
  };

export const updateSearchStateTerm =
  (term: string) => (dispatch: AppDispatch) => {
    if (!lodash.isString(term)) {
      return;
    }
    dispatch(updateSearchTerm(term));
  };
