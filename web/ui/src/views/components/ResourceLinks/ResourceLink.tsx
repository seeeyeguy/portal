import React from "react";
import { toast } from "react-toastify";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";
import FavoriteThumbnailLink from "views/components/FavoriteThumbnailLink/FavoriteThumbnailLink";
import { Fernet } from "fernet-ts";
import lodash from "lodash";

import { SERVER_ERROR } from "definitions/StatusCodeConstants";
import visitApi, {
  TApiPostVisitRequest,
} from "state/query/api/portal/analytics/AnalyticsApi";
import favoriteApi, {
  TApiFavoriteRequest,
} from "state/query/api/portal/preferences/FavoriteApi";
import { useAppDispatch } from "state/store/store";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";

import styles from "views/components/ResourceLinks/ResourceLink.module.css";

export interface IResourceLinkProps {
  id: number;
  name: string;
  description: string;
  url: string;
  thumbnail: string;
  primaryPointOfContact: string;
  secondaryPointOfContacts?: string[];
  download: boolean;
  restricted: boolean;
  favoriteId?: number | null | undefined;
}

const POINT_OF_CONTACT_PLACEHOLDER = "nathaniel.charbonneau@l3harris.com";

export default function ResourceLink({
  id,
  name,
  description,
  url,
  thumbnail,
  primaryPointOfContact,
  secondaryPointOfContacts,
  download,
  restricted,
  favoriteId = null,
}: IResourceLinkProps) {
  const dispatch = useAppDispatch();

  // Reduce errors if the button is pressed rapidly.
  const debouncedUpdateFavorites = React.useRef(
    lodash.debounce(() => updateFavorites(), 200, { leading: true })
  );

  const [isButtonActive, setIsButtonActive] =
    React.useState<boolean>(!!favoriteId);

  const [restrictedProps, setRestrictedProps] = React.useState({
    name,
    description,
    url,
  });

  React.useEffect(() => {
    const decryptProps = async () => {
      const fernet = await Fernet.getInstance(__DATA_ENCRYPTION_KEY__);
      const decryptedName = await fernet.decrypt(name);
      const decryptedDescription = await fernet.decrypt(description);
      const decryptedUrl = await fernet.decrypt(url);
      setRestrictedProps({
        name: decryptedName,
        description: decryptedDescription,
        url: decryptedUrl,
      });
    };
    if (restricted) {
      decryptProps();
    }
  }, [name, description, url, restricted, setRestrictedProps]);

  const memoizedPrimaryPointOfContact = React.useMemo(
    () =>
      primaryPointOfContact ?? "N/A",
    [primaryPointOfContact]
  );

  const memoizedSecondaryPointsOfContacts = React.useMemo(
    () => secondaryPointOfContacts ?? [],
    [secondaryPointOfContacts]
  );

  const updateFavorites = React.useCallback(async () => {
    if (!isButtonActive) {
      const body: TApiFavoriteRequest = { resource: id };
      const promise = dispatch(
        favoriteApi.endpoints.addFavorite.initiate(body)
      );
      const { error } = await promise;

      // Handle the addFavorite API error.
      if (error && (error as FetchBaseQueryError).status === SERVER_ERROR) {
        const message =
          "data" in error ? (error.data as string) : DEFAULT_API_ERROR_MESSAGE;
        setIsButtonActive(false);
        throw new Error(message);
      }
    } else {
      if (favoriteId) {
        const promise = dispatch(
          favoriteApi.endpoints.removeFavorite.initiate(favoriteId)
        );
        const { error } = await promise;

        // Handle the removeFavorite API error.
        if (error && (error as FetchBaseQueryError).status === SERVER_ERROR) {
          const message =
            "data" in error
              ? (error.data as string)
              : DEFAULT_API_ERROR_MESSAGE;
          setIsButtonActive(true);
          throw new Error(message);
        }
      }
    }
  }, [favoriteId, id, isButtonActive, dispatch, setIsButtonActive]);

  const onButtonClickError = React.useCallback((message?: string) => {
    toast.error(message);
  }, []);

  const onLinkClick = React.useCallback(async () => {
    const body: TApiPostVisitRequest = { resource: id };
    const promise = dispatch(visitApi.endpoints.addVisit.initiate(body));
    await promise;
  }, [id, dispatch]);

  return (
    <span
      className={styles["favorite-link-container"]}
      aria-description="styling container for a favorite link"
    >
      <FavoriteThumbnailLink
        className={styles["favorite-link"]}
        name={restrictedProps.name}
        description={restrictedProps.description}
        url={restrictedProps.url}
        imgWidth={95}
        imgHeight={95}
        thumbnail={thumbnail}
        download={download}
        rel="noreferrer"
        target="_blank"
        tooltipHTMLContent={
          memoizedPrimaryPointOfContact === POINT_OF_CONTACT_PLACEHOLDER &&
          memoizedSecondaryPointsOfContacts.length === 0 ? null : (
            <>
              <h4>Point of Contact:</h4>
              {memoizedPrimaryPointOfContact !== "N/A" && (
                <a href={`mailto:${memoizedPrimaryPointOfContact}`}>
                  {memoizedPrimaryPointOfContact}
                </a>
              )}
              {memoizedSecondaryPointsOfContacts.length > 0 && (
                <>
                  <h4>Secondary Point of Contact(s):</h4>
                  {memoizedSecondaryPointsOfContacts.map((email: string) => (
                    <div key={email}>
                      <a href={`mailto:${email}`}>{email}</a>
                    </div>
                  ))}
                </>
              )}
            </>
          )
        }
        isButtonActive={isButtonActive}
        isButtonDisabled={false}
        buttonClassName={styles["favorite-button"]}
        callback={onLinkClick}
        buttonCallback={debouncedUpdateFavorites.current}
        buttonErrorCallback={onButtonClickError}
        maxLineHeight={2}
      />
    </span>
  );
}
