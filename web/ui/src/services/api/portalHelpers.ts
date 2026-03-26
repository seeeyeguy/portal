import lodash from "lodash";

export const RESOURCE_PATHS = {
  ANALYTICS: "analytics",
  CONTENT: "content",
  DIRECTORY: "directory",
  PREFERENCES: "preferences",
  PROGRAM_REVIEW_TOOL: "program-review-tool",
  REQUEST: "request",
  USERS: "users",
} as const;

type RESOURCE_PATHS_KEYS = keyof typeof RESOURCE_PATHS;
type RESOURCE_PATHS = (typeof RESOURCE_PATHS)[RESOURCE_PATHS_KEYS];

type ANALYTICS_RESOURCE = "queries" | "visits";
type CONTENT_RESOURCE = "content";
type DIRECTORY_RESOURCE =
  | "employee-levels"
  | "functions"
  | "resources"
  | "subfunctions"
  | "tags";
type PREFERENCES_RESOURCE = "favorites" | "query-filter-state";
type PROGRAM_REVIEW_TOOL_RESOURCE =
  | "portfolio"
  | "program"
  | "record"
  | "reporting-period";
type REQUEST_RESOURCE = "disposition" | "request";
type USERS_RESOURCE = "access" | "access/subfunctions";
type RESOURCE =
  | ANALYTICS_RESOURCE
  | CONTENT_RESOURCE
  | DIRECTORY_RESOURCE
  | PREFERENCES_RESOURCE
  | PROGRAM_REVIEW_TOOL_RESOURCE
  | REQUEST_RESOURCE
  | USERS_RESOURCE;

type SUFFIX = "search" | "review" | null;

type PARAM =
  | "id"
  | "ids"
  | "key"
  | "label"
  | "page"
  | "pa_number"
  | "pa_numbers"
  | "role_levels"
  | "segments"
  | "subfunctions"
  | "stages"
  | "tiers"
  | "user";

const acceptedParamArrays = new Set([
  "ids",
  "pa_numbers",
  "role_levels",
  "segments",
  "subfunctions",
  "stages",
  "tiers",
]);

/**
 * Build a URL for an endpoint, given its application path,
 * resource name, suffix path, and appropriate query param.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @param suffix An optional suffix to append to the base URL.
 * @param paramType An appropriate query param to add to the URL.
 * @returns A function that accepts an optional query param and returns the appropriate URL.
 */
const buildQueryResourceURL =
  (
    path: RESOURCE_PATHS,
    resource: RESOURCE,
    suffix: SUFFIX,
    paramType: PARAM
  ) =>
  (param: number | number[] | string[] | string | null = null) => {
    const base = `${path}/${resource}${suffix ? `/${suffix}` : ""}`;
    if (param) {
      if (acceptedParamArrays.has(paramType)) {
        const queryParamArray = (param as number[] | string[]).reduce(
          (acc, arg, i) => {
            const queryParamArrayArg = `${paramType}=${arg}`;
            if (i < 1) {
              return `${acc}${queryParamArrayArg}`;
            }
            return `${acc}&${queryParamArrayArg}`;
          },
          ""
        );
        return `${base}?${queryParamArray}`;
      }
      return `${base}?${paramType}=${param}`;
    }
    return base;
  };

/**
 * Build a URL with an optional id for an endpoint, given its application path, and
 * resource name.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional id and returns the appropriate URL.
 */
export const buildQueryResourceByIdURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE
) => buildQueryResourceURL(path, resource, null, "id");

/**
 * Build a URL with an optional array of ids for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional array of ids and returns the appropriate URL.
 */
export const buildQueryResourceByIdsURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "ids");

/**
 * Build a URL with an optional key for an endpoint, given its application path, and
 * resource name.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional key and returns the appropriate URL.
 */
export const buildQueryResourceByKeyURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE
) => buildQueryResourceURL(path, resource, null, "key");

/**
 * Build a URL with an optional PA number for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional PA number and returns the appropriate URL.
 */
export const buildQueryResourceByPANumberURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "pa_number");

/**
 * Build a URL with an optional array of PA numbers for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional array of PA numbers and returns the appropriate URL.
 */
export const buildQueryResourceByPANumbersURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "pa_numbers");

/**
 * Build a URL with an optional array of role levels for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional array of role levels and returns the appropriate URL.
 */
export const buildQueryResourceByRoleLevelsURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "role_levels");

/**
 * Build a URL with an optional array of subfunctions for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional array of subfunctions and returns the appropriate URL.
 */
export const buildQueryResourceBySubFunctionsURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "subfunctions");

/**
 * Build a URL with an optional array of stages for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional array of stages and returns the appropriate URL.
 */
export const buildQueryResourceByStagesURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "stages");

/**
 * Build a URL with an optional array of tiers for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional array of tiers and returns the appropriate URL.
 */
export const buildQueryResourceByTiersURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "tiers");

/**
 * Build a URL with an optional array of segments for an endpoint given its
 * application path, resource name, and optional suffix.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional array of segments and returns the appropriate URL.
 */
export const buildQueryResourceBySegmentsURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE,
  suffix: SUFFIX = null
) => buildQueryResourceURL(path, resource, suffix, "segments");

/**
 * Build a URL with an optional user for an endpoint, given its application path, and
 * resource name.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional user and returns the appropriate URL.
 */
export const buildQueryResourceByUserURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE
) => buildQueryResourceURL(path, resource, null, "user");

/**
 * Build a URL with an optional label for an endpoint suffixed with /search,
 * given its application path, and resource name.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional label and returns the appropriate URL.
 */
export const buildSearchForResourceByLabelURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE
) => buildQueryResourceURL(path, resource, "search", "label");

/**
 * Build a URL with an optional page for an endpoint suffixed with /search,
 * given its application path, and resource name.
 * @param path The path/prefix denoting the resource's application domain.
 * @param resource The name of the resource.
 * @returns A function that accepts an optional page and returns the appropriate URL.
 */
export const buildSearchForResourceByPageURL = (
  path: RESOURCE_PATHS,
  resource: RESOURCE
) => buildQueryResourceURL(path, resource, "search", "page");

/**
 * General utility to append a query param to a URL.
 * @param base The base URL.
 * @param param The name of the query param to append.
 * @param paramValue The value of the query param to append.
 * @param matchPattern The pattern to match as to determine whether to append with an `&` or `?`.
 * @returns The URL with appended query param.
 */
export const appendQueryParamToURL = (
  base: string,
  param: string,
  paramValue: string | number | boolean | null,
  matchPattern: RegExp | null = /\?(.*?)=/
) =>
  !lodash.isNil(paramValue)
    ? `${base}${matchPattern && matchPattern.test(base) ? "&" : "?"}${param}=${paramValue}`
    : base;
