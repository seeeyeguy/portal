export interface Option {
  label: string;
  value: unknown;
}

/**
 * Create a dropdown option.
 *
 * @param {string} label label for option.
 * @param {unknown} value value for option.
 * @returns {Option} an object formatted as a dropdown option.
 */
export function transformToOption(label: string, value: unknown = null) {
  return { label, value: value ?? label };
}

/**
 * Create a list of dropdown options.
 *
 * @param {array} options a list of values.
 * @returns {Option[]} an array of options.
 */
export function transformToOptions(options: string[]) {
  return options.map((option) => transformToOption(option));
}

/**
 * Create a list of boolean dropdown options, using `truthyValue` to determine whether
 * the value of an option is true or false.
 * @param {array} booleanOptions a list of values to transform into options.
 * @param {unknown} truthyValue a value to be compared against to deem an option value as truthy.
 * @returns {Option[]} an array of options.
 */
export function transformToBooleanOptions(
  booleanOptions: string[],
  truthyValue: unknown
) {
  return booleanOptions.map((option) =>
    transformToOption(option, option === truthyValue)
  );
}
