import React from "react";

import styles from "views/components/MaintenanceBanner/MaintenanceBanner.module.css";

export type LogLevels = "INFO" | "SUCCESS" | "WARNING" | "CRITICAL";

export interface IMaintenanceBannerProps {
  level: LogLevels;
  header?: string;
  body?: string;
  subtext?: string;
  enabled: boolean;
  dismissable: boolean;
}

export default function MaintenanceBanner({
  level,
  header,
  body,
  subtext,
  enabled,
  dismissable,
}: IMaintenanceBannerProps) {
  const [disableBanner, setDisableBanner] = React.useState(!enabled);

  const onClickDisableBanner = React.useCallback(
    (event: React.MouseEvent) => {
      event.stopPropagation();
      setDisableBanner(true);
    },
    [setDisableBanner]
  );

  return (
    <div
      aria-description="container for maintenance banner"
    >
      {enabled && !disableBanner && (
        <div
          className={`${styles[`maintenance-banner-level-${level}`]} ${styles["maintenance-banner-content"]}`}
          aria-description="maintenance banner"
        >
          <div aria-description="container for maintenance banner content">
            {header && (
              <header>
                <h3>{header}</h3>
              </header>
            )}
            {body && <main>{body}</main>}
            {subtext && <footer>{subtext}</footer>}
          </div>
          <div aria-description="container for maintenance banner dismiss button">
            {dismissable && <button onClick={onClickDisableBanner}>X</button>}
          </div>
        </div>
      )}
    </div>
  );
}
