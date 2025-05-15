import { createSlice, PayloadAction } from "@reduxjs/toolkit";

import { ISearchParams } from "definitions/portal/directory/Resource.types";

export const initialState: ISearchParams = {
  search: { term: "", record: null },
  employeeLevels: [],
  functions: [],
  tags: [],
};

const ResourceSearchSlice = createSlice({
  name: "directoryResourceSearch",
  initialState,
  reducers: {
    clearDirectoryResourceSearch: () => ({
      ...initialState,
    }),
    clearEmployeeLevels: (state) => ({
      ...state,
      employeeLevels: initialState.employeeLevels,
    }),
    clearFilters: (state) => ({
      ...initialState,
      search: { ...state.search },
    }),
    clearFunctions: (state) => ({
      ...state,
      functions: initialState.functions,
    }),
    clearSearch: (state) => ({
      ...state,
      search: { ...initialState.search },
    }),
    clearTags: (state) => ({
      ...state,
      tags: initialState.tags,
    }),
    loadDirectoryResourceSearch: (_, action: PayloadAction<ISearchParams>) => ({
      ...action.payload,
    }),
    toggleEmployeeLevels: (state, action: PayloadAction<number>) => {
      const employeeLevelsSet = new Set(state.employeeLevels);
      if (employeeLevelsSet.has(action.payload)) {
        return {
          ...state,
          employeeLevels: state.employeeLevels.filter(
            (id) => id !== action.payload
          ),
        };
      }
      return {
        ...state,
        employeeLevels: [...state.employeeLevels, action.payload],
      };
    },
    toggleFunctions: (state, action: PayloadAction<number>) => {
      const functionsSet = new Set(state.functions);
      if (functionsSet.has(action.payload)) {
        return {
          ...state,
          functions: state.functions.filter((id) => id !== action.payload),
        };
      }
      return { ...state, functions: [...state.functions, action.payload] };
    },
    toggleTags: (state, action: PayloadAction<number>) => {
      const tagsSet = new Set(state.tags);
      if (tagsSet.has(action.payload)) {
        return {
          ...state,
          tags: state.tags.filter((id) => id !== action.payload),
        };
      }
      return { ...state, tags: [...state.tags, action.payload] };
    },
    updateSearchRecord: (state, action: PayloadAction<number>) => ({
      ...state,
      search: { ...state.search, record: action.payload },
    }),
    updateSearchTerm: (state, action: PayloadAction<string>) => ({
      ...state,
      search: { ...state.search, term: action.payload },
    }),
  },
});

export const {
  clearDirectoryResourceSearch,
  clearEmployeeLevels,
  clearFilters,
  clearFunctions,
  clearSearch,
  clearTags,
  loadDirectoryResourceSearch,
  toggleEmployeeLevels,
  toggleFunctions,
  toggleTags,
  updateSearchRecord,
  updateSearchTerm,
} = ResourceSearchSlice.actions;
export default ResourceSearchSlice.reducer;
