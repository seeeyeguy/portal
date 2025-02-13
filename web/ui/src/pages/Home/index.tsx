import React from "react";
import { useLoaderData } from "react-router";

import NavBar from "components/nav/NavBar";
import Controls from "containers/Controls";
import Favorites from "containers/Favorites";
import Results from "containers/Results";

import { loadDirectoryResourceSearchState } from "state/actions/portal/directory/Resource/Search";
import { useSearchTagsQuery } from "state/query/api/portal/directory/Tag";
import { useGetFavoritesQuery } from "state/query/api/portal/preferences/Favorite";
import { useGetProfileUserQuery } from "state/query/api/portal/users/Profile";
import { useAppDispatch } from "state/store";

import Tag from "state/types/portal/directory/Tag";
import Favorite from "state/types/portal/preferences/Favorite";
import Profile from "state/types/portal/users/Profile";
import type { User } from "state/types/services/sso";

const FILTER_PREFIX = "filter::";

export default function Home() {
  const loaderData = useLoaderData() as { user: User };

  const dispatch = useAppDispatch();

  const filterData = React.useRef<{ [key: string]: string[] }>(
    JSON.parse(localStorage.getItem("filterData") ?? "{}")
  );

  const { data: profileApiResponse } = useGetProfileUserQuery(
    loaderData.user.email
  );
  const profile = (profileApiResponse?.data ?? {
    user: {
      firstName: loaderData.user.firstName,
      lastName: loaderData.user.lastName,
      email: loaderData.user.email,
    },
    jobTitle: "UNKNOWN",
    citizenship: "UNKNOWN",
  }) as Profile;

  const { data: favoritesApiResponse } = useGetFavoritesQuery(
    loaderData.user.email
  );
  const favorites = (favoritesApiResponse?.data ?? []) as Favorite[];

  const { data: tagsApiResponse } = useSearchTagsQuery(FILTER_PREFIX);
  const filterTags = (tagsApiResponse?.data ?? []) as Tag[];

  // Load initial user session data.
  React.useEffect(() => {
    dispatch(loadDirectoryResourceSearchState(loaderData.user.email));
  }, [loaderData, dispatch]);

  if (!loaderData.user.email) {
    return <div>:x: 404</div>;
  }

  return (
    <>
      <NavBar profile={profile} />
      <div id="page-content">
        <Controls />
        <Favorites favorites={favorites} profile={profile} />
        <Results
          favorites={favorites}
          filterData={filterData}
          filterTags={filterTags}
          profile={profile}
        />
      </div>
    </>
  );
}
