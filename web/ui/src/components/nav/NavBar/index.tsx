import React from "react";
import { SearchBar } from "adas-react-components";
import type { Profile } from "adas-react-components/types";

import menuItems from "components/nav/NavBar/props/menu";

import { NavBarProps } from "components/nav/NavBar/types";

import endpoints from "routes/api/endpoints";
import {
  updateSearchStateRecord,
  updateSearchStateTerm,
} from "state/actions/portal/directory/Resource/Search";
import queryApi, {
  ApiQueryRequest,
} from "state/query/api/portal/analytics/Query";
import resourceApi, {
  ApiSearchResourceRequest,
} from "state/query/api/portal/directory/Resource";
import store from "state/store";

import Query from "state/types/portal/analytics/Query";
import Resource from "state/types/portal/directory/Resource";

import { transformToOption } from "utils/components/select/options";

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

  const loadSearchOptions = React.useCallback(async (term: string) => {
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
        limit: 5,
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

  const onSubmitSearch = React.useCallback(async (searchTerm: string) => {
    const body: ApiQueryRequest = { searchTerm };
    const promise = store.dispatch(queryApi.endpoints.addQuery.initiate(body));
    const response = await promise;
    const { data } = response?.data ?? { data: {} as Query };
    store.dispatch(updateSearchStateTerm(searchTerm));
    store.dispatch(updateSearchStateRecord(data));
  }, []);

  return (
    <SearchBar
      siteName="BI Portal"
      icon=""
      menuItems={menuItems}
      contactUsEmail={CONTACT_US_EMAIL}
      logoutHref={endpoints.SERVICE.SSO.LOGOUT}
      profile={profileData}
      clearOnSubmit={true}
      isSearchDisabled={false}
      searchOptions={loadSearchOptions}
      onSubmitSearch={onSubmitSearch}
    />
  );
}
