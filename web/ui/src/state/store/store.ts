import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import logger from "redux-logger";

import api from "state/query/api";
import AppReducers from "state/slices";

import { inDevelopment } from "definitions/EnviormentConstants";

const middleware = [api.middleware];

if (inDevelopment()) {
  middleware.push(logger);
}

const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    ...AppReducers,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(middleware),
});

export default store;

export type AppDispatch = typeof store.dispatch;
export const useAppDispatch: () => AppDispatch = useDispatch;
export type RootState = ReturnType<typeof store.getState>;
export const useTypedSelector: TypedUseSelectorHook<RootState> = useSelector;
