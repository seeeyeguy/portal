import FavoriteButton from "views/components/FavoriteButton/FavoriteButton";
import ThumbnailLink from "views/components/ThumbnailLink/ThumbnailLink";

import { ThumbnailLinkProps } from "views/components/ThumbnailLink/ThumbnailLink";

export interface FavoriteThumbnailLinkProps
  extends Omit<ThumbnailLinkProps, "rightOfLabelContent"> {
  isButtonActive: boolean;
  isButtonDisabled: boolean;
  buttonClassName: string;
  buttonCallback: () => void;
  buttonErrorCallback: (message?: string) => void;
}

export default function FavoriteThumbnailLink({
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
  isButtonActive = false,
  isButtonDisabled = false,
  buttonClassName = "",
  leftOfLabelContent = null,
  callback = () => undefined,
  buttonCallback = () => undefined,
  buttonErrorCallback = () => undefined,
}: FavoriteThumbnailLinkProps) {
  return (
    <ThumbnailLink
      name={name}
      description={description}
      url={url}
      thumbnail={thumbnail}
      imgWidth={imgWidth}
      imgHeight={imgHeight}
      download={download || undefined}
      referrerPolicy={referrerPolicy}
      rel={rel}
      target={target}
      className={className}
      showTooltip={showTooltip}
      tooltipPlace={tooltipPlace}
      tooltipDelay={tooltipDelay}
      tooltipHTMLContent={tooltipHTMLContent}
      maxLineHeight={maxLineHeight}
      leftOfLabelContent={leftOfLabelContent}
      rightOfLabelContent={
        <FavoriteButton
          isActive={isButtonActive}
          disabled={isButtonDisabled}
          className={buttonClassName}
          callback={buttonCallback}
          errorCallback={buttonErrorCallback}
        />
      }
      callback={callback}
    />
  );
}
