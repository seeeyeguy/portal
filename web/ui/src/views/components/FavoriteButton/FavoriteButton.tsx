import React from "react";
import { faStar as farStarThin } from "@fortawesome/free-regular-svg-icons";
import { faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "./FavoriteButton.module.css";

export interface FavoriteButtonProps {
  isActive: boolean;
  disabled: boolean;
  className: string;
  callback: () => void | Promise<unknown>;
  errorCallback: (message?: string) => void;
}

export default function FavoriteButton({
  isActive,
  disabled,
  className,
  callback,
  errorCallback,
}: FavoriteButtonProps) {
  const [active, setActive] = React.useState(isActive);

  React.useEffect(() => {
    setActive(isActive);
  }, [isActive]);

  const favoriteItem = React.useCallback(
    async (event: React.MouseEvent) => {
      event.stopPropagation();
      try {
        setActive((state) => !state);
        await callback();
      } catch (error) {
        setActive(isActive);
        errorCallback((error as Error).message);
      }
    },
    [isActive, callback, errorCallback, setActive]
  );

  return (
    <button
      disabled={disabled}
      className={`${className} ${styles["favorite-button"]}`}
      onClick={favoriteItem}
    >
      {active ? (
        <FontAwesomeIcon icon={faStar} data-testid="faStar-icon" />
      ) : (
        <FontAwesomeIcon icon={farStarThin} data-testid="faStarThin-icon" />
      )}
    </button>
  );
}
