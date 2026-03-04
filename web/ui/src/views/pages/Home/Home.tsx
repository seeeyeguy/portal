import React from "react";
import { useLoaderData } from "react-router";

import FAQModal from "views/components/FAQModal/FAQModal";
import IntroModal from "views/components/IntroModal/IntroModal";
import NavBar from "views/components/NavBar/NavBar";
import PageContent from "views/components/PageContent/PageContent";
import Controls from "views/containers/Controls/Controls";
import Favorites from "views/containers/Favorites/Favorites";
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import Results from "views/containers/Results/Results";

import { loadDirectoryResourceSearchState } from "state/actions/ResourceSearchActions";
import { useSearchTagsQuery } from "state/query/api/portal/directory/TagApi";
import { useGetFavoritesQuery } from "state/query/api/portal/preferences/FavoriteApi";
import { useGetProfileUserQuery } from "state/query/api/portal/users/UsersApi";
import { useAppDispatch } from "state/store/store";

import { ITag } from "definitions/portal/directory/Tag.types";
import { IFavorite } from "definitions/portal/preferences/Favorite.types";
import { IProfile } from "definitions/portal/users/Profile.types";
import type { IAuthUser } from "definitions/Sso.types";

const FILTER_PREFIX = "filter::";

export default function Home() {
  const loaderData = useLoaderData() as { user: IAuthUser };

  const dispatch = useAppDispatch();

  // Refs to manipulate navbar profile menu.
  const smNavBarRef = React.useRef<HTMLElement>(null);
  const mdNavBarRef = React.useRef<HTMLElement>(null);
  const lgNavBarRef = React.useRef<HTMLElement>(null);

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
      username: loaderData.user.username,
    },
    jobTitle: "UNKNOWN",
    citizenship: "UNKNOWN",
  }) as IProfile;

  const { data: favoritesApiResponse } = useGetFavoritesQuery(
    loaderData.user.username
  );
  const favorites = (favoritesApiResponse?.data ?? []) as IFavorite[];

  const { data: tagsApiResponse } = useSearchTagsQuery(FILTER_PREFIX);
  const filterTags = (tagsApiResponse?.data ?? []) as ITag[];

  const closeNavBarProfile = React.useCallback(() => {
    if (smNavBarRef.current) {
      smNavBarRef.current.click();
    }
    if (mdNavBarRef.current) {
      mdNavBarRef.current.click();
    }
    if (lgNavBarRef.current) {
      lgNavBarRef.current.click();
    }
  }, []);

  // Load initial user session data.
  React.useEffect(() => {
    dispatch(loadDirectoryResourceSearchState(loaderData.user.username));
  }, [loaderData, dispatch]);

  React.useLayoutEffect(() => {
    const computePaddingBottom = () => {
      const banner = document.querySelector(
        'div[class*="maintenance-banner-level"]'
      );
      const content = document.getElementById("page-content");

      if (banner && content) {
        content.style.paddingBottom = "3rem";
      }
      else if (content) {
        content.style.paddingBottom = "initial";
      }
    };

    const targetNode = document.getElementById("root");

    if (!targetNode) {
      return;
    }

    const callback = (mutationsList: MutationRecord[]) => {
      for (const mutation of mutationsList) {
        if (mutation.type === "childList" || mutation.type === "attributes") {
          computePaddingBottom();
        }
      }
    };

    const observer = new MutationObserver(callback);
    const config = { childList: true, subtree: true, attributes: true };
    observer.observe(targetNode, config);

    return () => observer.disconnect();
  }, []);

  if (!loaderData.user.email) {
    return <div>:x: 404</div>;
  }

  return (
    <>
      <MaintenanceBanner page="/" />
      <div
        id="app-container"
        onClick={() => {
          closeNavBarProfile();
        }}
        aria-description="container for main application"
      >
        <FAQModal />
        <IntroModal />
        <NavBar
          profile={profile}
          navBarRefs={[smNavBarRef, mdNavBarRef, lgNavBarRef]}
        />
        <PageContent>
          <Controls />
          <Favorites favorites={favorites} profile={profile} />
          <Results
            favorites={favorites}
            filterData={filterData}
            filterTags={filterTags}
            profile={profile}
          />
        </PageContent>
      </div>
    </>
  );
}
