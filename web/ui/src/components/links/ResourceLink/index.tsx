import React from "react";
import { toast } from "react-toastify";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";
import { FavoriteThumbnailLink } from "adas-react-components";
import lodash from "lodash";

import { ResourceLinkProps } from "components/links/ResourceLink/types";

import { SERVER_ERROR } from "routes/api/helpers/headers/status-codes";
import visitApi, {
  ApiVisitRequest,
} from "state/query/api/portal/analytics/Visit";
import favoriteApi, {
  ApiFavoriteRequest,
} from "state/query/api/portal/preferences/Favorite";
import { useAppDispatch } from "state/store";

import { DEFAULT_API_ERROR_MESSAGE } from "utils/constants/errors";

import styles from "components/links/ResourceLink/styles/index.module.css";

export default function ResourceLink({
  id,
  name,
  description,
  url,
  thumbnail,
  download,
  favoriteId = null,
}: ResourceLinkProps) {
  const dispatch = useAppDispatch();

  // Reduce errors if the button is pressed rapidly.
  const debouncedUpdateFavorites = React.useRef(
    lodash.debounce(() => updateFavorites(), 200, { leading: true })
  );

  const [isButtonActive, setIsButtonActive] =
    React.useState<boolean>(!!favoriteId);

  const updateFavorites = React.useCallback(async () => {
    if (!isButtonActive) {
      const body: ApiFavoriteRequest = { resource: id };
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
    const body: ApiVisitRequest = { resource: id };
    const promise = dispatch(visitApi.endpoints.addVisit.initiate(body));
    await promise;
  }, [id, dispatch]);

  return (
    <FavoriteThumbnailLink
      className={styles["favorite-link"]}
      name={name}
      description={description}
      url={url}
      imgWidth={95}
      imgHeight={95}
      thumbnail={thumbnail}
      download={download}
      rel="noreferrer"
      target="_blank"
      isButtonActive={isButtonActive}
      isButtonDisabled={false}
      buttonClassName={styles["favorite-button"]}
      callback={onLinkClick}
      buttonCallback={debouncedUpdateFavorites.current}
      buttonErrorCallback={onButtonClickError}
    />
  );
}
