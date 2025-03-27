import React from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { SearchBar } from "adas-react-components";
import type {
  Option,
  Profile as SearchBarProfile,
} from "adas-react-components/types";
import { faUndo } from "@fortawesome/free-solid-svg-icons";

import lodash from "lodash";

import menuItems from "views/components/NavBar/NavBarProps";

import endpoints from "services/api";
import { updateSearchStateTerm } from "state/actions/ResourceSearchActions";
import queryApi, {
  TApiQueryRequest,
} from "state/query/api/portal/analytics/AnalyticsApi";
import resourceApi, {
  TApiSearchResourceRequest,
} from "state/query/api/portal/directory/ResourceApi";
import {
  clearDirectoryResourceSearch,
  clearSearch,
} from "state/slices/ResourceSearchActions";
import store, { useAppDispatch, useTypedSelector } from "state/store/store";

import { IResource } from "definitions/portal/directory/Resource.types";
import { IProfile } from "definitions/portal/Users.types";

import { transformToOption } from "views/utils/OptionsUtility";
import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";

import styles from "views/components/NavBar/NavBar.module.css";

const CONTACT_US_EMAIL = "SAS-Portal@L3Harris.com";

const PROFILE: SearchBarProfile = {
  firstName: "",
  lastName: "",
  jobTitle: "",
  citizenship: "",
  icon: null,
};

export interface INavBarProps {
  profile: IProfile;
  hideSearchBar?: boolean;
}

export default function NavBar({
  profile,
  hideSearchBar = false,
}: INavBarProps) {
  const profileData = {
    ...PROFILE,
    firstName: profile?.user.firstName,
    lastName: profile?.user.lastName,
    jobTitle: profile?.jobTitle,
    citizenship: profile?.citizenship,
  };

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const searchTerm = useTypedSelector(
    (state) => state.ResourceSearch.search.term
  );

  const menuLinks = React.useMemo(
    () =>
      menuItems.map((menuItem) => ({
        ...menuItem,
        onClick: (event: React.MouseEvent) => {
          event.preventDefault();
          navigate(menuItem.path);
        },
      })),
    [navigate]
  );

  const clearSearchForSession = React.useCallback(
    () => dispatch(clearSearch()),
    [dispatch]
  );

  const clearSession = React.useCallback(
    () => dispatch(clearDirectoryResourceSearch()),
    [dispatch]
  );

  const querySearchOptions = React.useCallback(async (term: string) => {
    if (!term?.length) {
      return [];
    }

    const body: TApiSearchResourceRequest = {
      name: term,
      description: term,
      functions: [],
      subfunctions: [],
      employeeLevels: [],
      tags: [],
      download: null,
      structure: "default",
    };

    const promise = store.dispatch(
      resourceApi.endpoints.searchResources.initiate({
        body,
        page: null,
        limit: 30,
      })
    );
    const response = await promise;
    const { data: resources } = response?.data ?? { data: [] };

    return (
      (resources as IResource[]).map((resource) =>
        transformToOption(resource.name)
      ) ?? []
    );
  }, []);

  const debouncedQuerySearchOptions = React.useRef(
    lodash.debounce(
      async (value: string, callback: (options: Option[]) => void) => {
        const options = await querySearchOptions(value);
        callback(options);
      },
      300
    )
  );

  const loadSearchOptions = (value: string) =>
    new Promise<Option[]>((resolve) => {
      if (debouncedQuerySearchOptions.current) {
        debouncedQuerySearchOptions.current(value, resolve);
      }
    });

  const closeResourceAccordions = () => {
    const openAccordions = document.querySelectorAll(
      'details[class*="recursive-accordion"] > summary:has(div[aria-checked="true"])'
    );

    openAccordions.forEach((openAccordion) =>
      (openAccordion as HTMLElement).click()
    );
  };

  const onSubmitSearch = React.useCallback(async (newSearchTerm: string) => {
    store.dispatch(updateSearchStateTerm(newSearchTerm));

    const body: TApiQueryRequest = { searchTerm: newSearchTerm };
    const promise = store.dispatch(queryApi.endpoints.addQuery.initiate(body));
    const { error } = await promise;
    const isError = !!error;

    if (isError) {
      if (error) {
        const message =
          "data" in error ? (error.data as string) : DEFAULT_API_ERROR_MESSAGE;
        toast.error(message);
      }
    }
  }, []);

  return (
    <SearchBar
      siteName=""
      icon="icon/portal-logo.png"
      iconHeight={37}
      iconWidth={150}
      menuProfileButtonIcon={
        <span className={styles["menu-button-icon"]}>
          {profileData?.firstName?.charAt(0) ?? "-"}
          {profileData?.lastName?.charAt(0) ?? "-"}
        </span>
      }
      menuItems={menuLinks}
      formButtons={[
        {
          label: "Reset View",
          className: styles["reset-view-button"],
          icon: faUndo,
          onClick: () => {
            clearSession();
            updateSearchStateTerm("");
            closeResourceAccordions();
          },
        },
      ]}
      contactUsEmail={CONTACT_US_EMAIL}
      logoutHref={endpoints.SERVICE.SSO.LOGOUT}
      profile={profileData}
      clearOnSubmit={false}
      hideSearch={hideSearchBar}
      isSearchDisabled={false}
      initialInput={searchTerm}
      searchOptions={loadSearchOptions}
      onSubmitSearch={onSubmitSearch}
      onSubmitSelect={onSubmitSearch}
      onClearSelect={() => {
        // Not passed directly so that void is returned.
        clearSearchForSession();
      }}
    />
  );
}
