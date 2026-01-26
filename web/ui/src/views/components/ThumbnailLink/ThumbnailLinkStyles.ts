/**
 * Generate dynamic styles for the `ThumbnailLink` component.
 * @param maxLineHeight The number of lines allowed in element before handling overflow.
 * @returns {React.CSSProperties} A styles object.
 */
export function thumbnailLinkStyles(
  maxLineHeight: number
): React.CSSProperties {
  return {
    WebkitLineClamp: `${Math.max(1, maxLineHeight ?? 1)}`,
  };
}
