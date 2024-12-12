import * as changeCase from "change-case";
import lodash from "lodash";

interface Dictionary {
  [key: string]: unknown;
}

type ListOrDictionary = Dictionary | unknown[];

type CaseType = "camelCase" | "snakeCase";

const caseTransforms = {
  camelCase: changeCase.camelCase,
  snakeCase: changeCase.snakeCase,
} as const;

/**
 * Transform dataset object keys to desired casing.
 * @param data Data object with keys, or nested object with keys to be transformed to
 * desired casing.
 * @param caseType Supported variable naming convention (camelCase, snake_case, etc).
 * @returns A transformed dataset with the appropriate casing.
 */
function caseTransformFunction(
  data: ListOrDictionary,
  caseType: CaseType
): ListOrDictionary {
  if (lodash.isArray(data)) {
    return data.map((item) => {
      if (lodash.isArray(item) || lodash.isPlainObject(item)) {
        return caseTransformFunction(item as ListOrDictionary, caseType);
      }
      return item;
    });
  }
  return lodash.entries(data).reduce((acc, tuple) => {
    let value = tuple[1];
    if (lodash.isArray(value) || lodash.isPlainObject(value)) {
      value = caseTransformFunction(value as Dictionary, caseType);
    }
    const newKey = caseTransforms[caseType](tuple[0] as string);
    acc[newKey] = value;
    return acc;
  }, {} as Dictionary);
}

/**
 * Transform dataset object keys from snake_case to camelCase.
 * @param data Data with snake_cased keys to be transformed to camelCase.
 * @returns A transformed dataset with the appropriate casing.
 */
export function snakeCaseToCamelCase(data: ListOrDictionary): ListOrDictionary {
  return caseTransformFunction(data, "camelCase");
}

/**
 * Transform dataset object keys from camelCase to snake_case.
 * @param data Data with camelCased keys to be transformed to snake_case.
 * @returns A transformed dataset with the appropriate casing.
 */
export function camelCaseToSnakeCase(data: ListOrDictionary): ListOrDictionary {
  return caseTransformFunction(data, "snakeCase");
}
