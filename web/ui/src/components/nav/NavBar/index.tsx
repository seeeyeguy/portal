import React from "react";
import { toast } from "react-toastify";
import { SearchBar } from "adas-react-components";
import type { Option, Profile } from "adas-react-components/types";
import lodash from "lodash";

import menuItems from "components/nav/NavBar/props/menu";

import { NavBarProps } from "components/nav/NavBar/types";

import endpoints from "routes/api/endpoints";
import { updateSearchStateTerm } from "state/actions/portal/directory/Resource/Search";
import queryApi, {
  ApiQueryRequest,
} from "state/query/api/portal/analytics/Query";
import resourceApi, {
  ApiSearchResourceRequest,
} from "state/query/api/portal/directory/Resource";
import {
  clearDirectoryResourceSearch,
  clearSearch,
} from "state/slices/portal/directory/Resource/Search";
import store, { useAppDispatch, useTypedSelector } from "state/store";

import Resource from "state/types/portal/directory/Resource";

import { transformToOption } from "utils/components/select/options";
import { DEFAULT_API_ERROR_MESSAGE } from "utils/constants/errors";

const CONTACT_US_EMAIL = "melissa.cataldo@l3harris.com";

const PROFILE: Profile = {
  firstName: "",
  lastName: "",
  jobTitle: "",
  citizenship: "",
  icon: null,
};

export default function NavBar({ profile }: NavBarProps) {
  const profileData = {
    ...PROFILE,
    firstName: profile?.user.firstName,
    lastName: profile?.user.lastName,
    jobTitle: profile?.jobTitle,
    citizenship: profile?.citizenship,
  };

  const dispatch = useAppDispatch();

  const searchTerm = useTypedSelector(
    (state) => state.ResourceSearch.search.term
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

    const body: ApiSearchResourceRequest = {
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
      (resources as Resource[]).map((resource) =>
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

  const onSubmitSearch = React.useCallback(async (newSearchTerm: string) => {
    store.dispatch(updateSearchStateTerm(newSearchTerm));

    const body: ApiQueryRequest = { searchTerm: newSearchTerm };
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
      siteName="BI Portal"
      icon=""
      menuItems={menuItems}
      contactUsEmail={CONTACT_US_EMAIL}
      logoutHref={endpoints.SERVICE.SSO.LOGOUT}
      profile={profileData}
      clearOnSubmit={false}
      isSearchDisabled={false}
      showSubmit={false}
      initialInput={searchTerm}
      searchOptions={loadSearchOptions}
      onSubmitSearch={onSubmitSearch}
      onSubmitSelect={onSubmitSearch}
      onClearSelect={() => {
        // Not passed directly so that void is returned.
        clearSearchForSession();
      }}
      menuButton={{
        label: "Reset View",
        onClick: () => {
          clearSession();
          updateSearchStateTerm("");
        },
      }}
    />
  );
}
