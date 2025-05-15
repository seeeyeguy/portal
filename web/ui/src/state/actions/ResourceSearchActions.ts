import lodash from "lodash";

import queryFilterStateApi, {
  TApiQueryFilterStateMutationRequest,
} from "state/query/api/portal/preferences/QueryFilterStateApi";
import {
  loadDirectoryResourceSearch,
  toggleEmployeeLevels,
  toggleFunctions,
  toggleTags,
  updateSearchRecord,
  updateSearchTerm,
} from "state/slices/ResourceSearchActions";
import { AppDispatch } from "state/store/store";

import { IQuery } from "definitions/portal/Analytics.types";
import { ISearchParams } from "definitions/portal/directory/Resource.types";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";

export const loadDirectoryResourceSearchState =
  (user: string) => async (dispatch: AppDispatch) => {
    const promise = dispatch(
      queryFilterStateApi.endpoints.getQueryFilterState.initiate(user)
    );
    const { data: response, error, isSuccess, isError } = await promise;
    const payload: ISearchParams = {
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
    queryFilterStateId: number | null = null
  ) =>
  (id: number) =>
  async (dispatch: AppDispatch) => {
    if (!lodash.isInteger(id)) {
      return;
    }

    dispatch(toggleEmployeeLevels(id));

    const body: TApiQueryFilterStateMutationRequest = {
      functions: functions,
      employeeLevels: lodash.xor(employees, [id]),
      search: null,
      tags: [],
    };

    dispatch(
      queryFilterStateApi.endpoints.postQueryFilterState.initiate({
        body,
        post: !queryFilterStateId,
        id: queryFilterStateId,
      })
    );
  };

export const toggleFunction =
  (
    functions: number[],
    employees: number[],
    queryFilterStateId: number | null = null
  ) =>
  (id: number) =>
  async (dispatch: AppDispatch) => {
    if (!lodash.isInteger(id)) {
      return;
    }

    dispatch(toggleFunctions(id));

    const body: TApiQueryFilterStateMutationRequest = {
      functions: lodash.xor(functions, [id]),
      employeeLevels: employees,
      search: null,
      tags: [],
    };

    dispatch(
      queryFilterStateApi.endpoints.postQueryFilterState.initiate({
        body,
        post: !queryFilterStateId,
        id: queryFilterStateId,
      })
    );
  };

export const toggleTag = (id: number) => (dispatch: AppDispatch) => {
  if (!lodash.isInteger(id)) {
    return;
  }
  dispatch(toggleTags(id));
};

export const updateSearchStateRecord =
  (record: IQuery) => (dispatch: AppDispatch) => {
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
