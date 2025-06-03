/**
 * Calculates the font size (vw) based on the length of the input string.
 *
 * @param {string} defaultFontSize - The default font size to use if the input is not provided or is shorter than the cutoff.
 * @param {number} fontSizeSlope - The slope of the decay function controlling how quickly the font size decreases.
 * @param {number} inputCutoff - The number of characters after which the font size starts to decrease.
 * @param {number} maxFontSize - The maximum font size.
 * @param {number} minFontSize - The minimum font size that we approach.
 * @param {string} input - The input string whose length determines the font size.
 *
 * @returns {string} - The calculated font size in viewport width (vw) units or the default font size.
 */
export function calculateFontSize(
  defaultFontSize: string,
  fontSizeSlope: number,
  inputCutoff: number,
  maxFontSize: number,
  minFontSize: number,
  input?: string
) {
  if (input && input.length > inputCutoff) {
    const excessLength = input.length - inputCutoff;
    const fontSize =
      minFontSize +
      (maxFontSize - minFontSize) * Math.exp(-fontSizeSlope * excessLength);

    return `${fontSize}vw`;
  } else {
    return defaultFontSize;
  }
}
