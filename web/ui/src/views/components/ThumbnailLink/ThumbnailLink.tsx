import React from "react";
import { Tooltip } from "react-tooltip";
import { v4 as uuid } from "uuid";

import styles from "./ThumbnailLink.module.css";
import { thumbnailLinkStyles } from "./ThumbnailLinkStyles";

export interface ThumbnailLinkProps {
  name: string;
  description: string;
  url: string;
  thumbnail: string;
  imgWidth: number;
  imgHeight: number;
  download?: boolean | null;
  referrerPolicy?:
    | "strict-origin-when-cross-origin"
    | "same-origin"
    | "no-referrer";
  rel?: "" | "external" | "next" | "noopener" | "noreferrer" | "prev";
  target?: "_self" | "_blank";
  className?: string;
  showTooltip?: boolean;
  tooltipPlace?:
    | "top"
    | "top-start"
    | "top-end"
    | "right"
    | "right-start"
    | "right-end"
    | "bottom"
    | "bottom-start"
    | "bottom-end"
    | "left"
    | "left-start"
    | "left-end";
  tooltipDelay?: number;
  tooltipHTMLContent?: React.ReactNode;
  maxLineHeight?: number;
  leftOfLabelContent?: React.ReactNode | null;
  rightOfLabelContent?: React.ReactNode | null;
  callback?: () => void | Promise<unknown>;
}

export default function ThumbnailLink({
  name,
  description,
  url,
  thumbnail,
  imgWidth,
  imgHeight,
  download,
  referrerPolicy = "strict-origin-when-cross-origin",
  rel = "",
  target = "_self",
  className = "",
  showTooltip = true,
  tooltipPlace = "left-start",
  tooltipDelay = 1000,
  tooltipHTMLContent = <></>,
  maxLineHeight = 1,
  leftOfLabelContent = null,
  rightOfLabelContent = null,
  callback = () => undefined,
}: ThumbnailLinkProps) {
  const thumbnailId = React.useMemo(() => uuid(), []);

  const navigateToTarget = React.useCallback(() => {
    const anchor = document.createElement("a");
    if (download) {
      anchor.download = `${download}`;
    }
    anchor.href = url;
    anchor.referrerPolicy = referrerPolicy;
    anchor.rel = rel;
    anchor.target = target;
    anchor.click();
  }, [download, referrerPolicy, rel, target, url]);

  const onClick = React.useCallback(
    async (event: React.MouseEvent) => {
      event.preventDefault();
      await callback();
      navigateToTarget();
    },
    [callback, navigateToTarget]
  );

  return (
    <>
      <div
        className={styles["thumbnail-link-container"]}
        aria-description="thumbnail link container"
      >
        {leftOfLabelContent}
        <a
          className={`${className} ${styles["thumbnail-link"]}`}
          href={url}
          target={target}
          referrerPolicy={referrerPolicy}
          rel={rel}
          download={download ?? undefined}
          onClick={onClick}
          data-tooltip-id={`thumbnail-link-description-tooltip-${thumbnailId}`}
          data-tooltip-delay-show={tooltipDelay}
        >
          <img
            className={`${styles["thumbnail-link-img"]}`}
            src={thumbnail}
            alt={description}
            width={imgWidth}
            height={imgHeight}
          />
          <div
            style={thumbnailLinkStyles(maxLineHeight)}
            className={`${styles["thumbnail-link-content-container"]}`}
            aria-description="thumbnail link content container"
          >
            {name}
          </div>
        </a>
        {rightOfLabelContent}
      </div>
      {showTooltip && (
        <Tooltip
          id={`thumbnail-link-description-tooltip-${thumbnailId}`}
          className={styles["thumbnail-link-description-tooltip"]}
          place={tooltipPlace}
          clickable
        >
          <h3>{name}</h3>
          <p>{description}</p>
          <div
            className="thumbnail-link-tooltip-html"
            aria-description="container for html content related to the description"
          >
            {tooltipHTMLContent}
          </div>
        </Tooltip>
      )}
    </>
  );
}
