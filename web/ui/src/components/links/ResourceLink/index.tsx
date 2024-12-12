import React from "react";
import { toast } from "react-toastify";
import { FavoriteThumbnailLink } from "adas-react-components";

import { ResourceLinkProps } from "components/links/ResourceLink/types";

import { CREATED, OK } from "routes/api/helpers/headers/status-codes";
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

  const [isButtonActive, setIsButtonActive] =
    React.useState<boolean>(!!favoriteId);

  const onButtonClick = React.useCallback(async () => {
    if (isButtonActive) {
      const body: ApiFavoriteRequest = { resource: id };
      const promise = dispatch(
        favoriteApi.endpoints.addFavorite.initiate(body)
      );
      const { data, error } = await promise;
      if (error) {
        const message =
          "data" in error ? (error.data as string) : DEFAULT_API_ERROR_MESSAGE;
        throw new Error(message);
      }
      const { status } = data ?? {};
      setIsButtonActive(status === CREATED);
    } else {
      if (favoriteId) {
        const promise = dispatch(
          favoriteApi.endpoints.removeFavorite.initiate(favoriteId)
        );
        const { data, error } = await promise;
        if (error) {
          const message =
            "data" in error
              ? (error.data as string)
              : DEFAULT_API_ERROR_MESSAGE;
          throw new Error(message);
        }
        const { status } = data ?? {};
        setIsButtonActive(status !== OK);
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
      isButtonDisabled={true}
      buttonClassName={styles["hidden-favorite-button"]}
      callback={onLinkClick}
      buttonCallback={onButtonClick}
      buttonErrorCallback={onButtonClickError}
    />
  );
}
