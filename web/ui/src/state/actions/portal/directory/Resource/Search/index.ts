import lodash from "lodash";

import Query from "state/types/portal/analytics/Query";

import {
  toggleEmployeeLevels,
  toggleFunctions,
  toggleTags,
  updateSearchRecord,
  updateSearchTerm,
} from "state/slices/portal/directory/Resource/Search";
import { AppDispatch } from "state/store";

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
    const isQueryRecord = !(
      lodash.difference(lodash.keys(record), queryRecordFields).length === 0
    );
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
