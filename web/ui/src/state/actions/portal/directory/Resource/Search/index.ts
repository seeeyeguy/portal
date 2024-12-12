import lodash from "lodash";

import queryFilterStateApi from "state/query/api/portal/preferences/QueryFilterState";
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

export const toggleEmployeeLevel = (id: number) => (dispatch: AppDispatch) => {
  if (!lodash.isInteger(id)) {
    return;
  }
  dispatch(toggleEmployeeLevels(id));
};

export const toggleFunction = (id: number) => (dispatch: AppDispatch) => {
  if (!lodash.isInteger(id)) {
    return;
  }
  dispatch(toggleFunctions(id));
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
