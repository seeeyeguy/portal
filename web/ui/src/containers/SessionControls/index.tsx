import React from "react";
import { Tooltip } from "react-tooltip";

import LoadSessionButton from "components/buttons/LoadSessionButton";
import SaveSessionButton from "components/buttons/SaveSessionButton";

import { SessionControlsProps } from "containers/SessionControls/types";

import {
  clearDirectoryResourceSearch,
  clearSearch,
} from "state/slices/portal/directory/Resource/Search";
import { useAppDispatch, useTypedSelector } from "state/store";

import styles from "containers/SessionControls/styles/index.module.css";

const TOOLTIP_ID = "clear-search-button-tooltip";

export default function SessionControls({
  filterData,
  filterTags,
}: SessionControlsProps) {
  const dispatch = useAppDispatch();
  const searchTerm = useTypedSelector(
    (state) => state.ResourceSearch.search.term
  );

  const clearSession = React.useCallback(
    () => dispatch(clearDirectoryResourceSearch()),
    [dispatch]
  );

  const clearSearchForSession = React.useCallback(
    () => dispatch(clearSearch()),
    [dispatch]
  );

  return (
    <div
      className={styles["session-controls"]}
      aria-description="container for buttons to control stored session data"
    >
      <div aria-description="container for buttons to clear session data">
        <button className={styles["session-buttons"]} onClick={clearSession}>
          Reset Session
        </button>
        <button
          className={styles["session-buttons"]}
          onClick={clearSearchForSession}
          data-tooltip-delay={1000}
          data-tooltip-id={TOOLTIP_ID}
        >
          Reset Search
        </button>
      </div>
      <div aria-description="container for buttons to load and save session data">
        <LoadSessionButton
          filterData={filterData}
          className={styles["session-buttons"]}
        />
        <SaveSessionButton
          filterData={filterData}
          filterTags={filterTags}
          className={styles["session-buttons"]}
        />
      </div>
      <Tooltip
        id={TOOLTIP_ID}
        className={styles["clear-search-session-button-tooltip"]}
        place="top-end"
      >
        {`Current Search Term: ${searchTerm?.length ? searchTerm : "N/A"}`}
      </Tooltip>
    </div>
  );
}
