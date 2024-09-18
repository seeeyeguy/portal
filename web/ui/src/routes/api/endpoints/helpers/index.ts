export const RESOURCE_PATHS = {
  ANALYTICS: "analytics",
  DIRECTORY: "directory",
  PREFERENCES: "preferences",
  USERS: "users",
} as const;

type RESOURCE_PATHS_KEYS = keyof typeof RESOURCE_PATHS;
type RESOURCE_PATHS = typeof RESOURCE_PATHS[RESOURCE_PATHS_KEYS];

type DIRECTORY_RESOURCE =
  | "employee-levels"
  | "functions"
  | "resources"
  | "subfunctions"
  | "tags";
type PREFERENCES_RESOURCE = "favorites" | "query-filter-state";
type RESOURCE = DIRECTORY_RESOURCE | PREFERENCES_RESOURCE;

type SUFFIX = "search" | null;

type PARAM = "id" | "label" | "page" | "user";

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
  (param: number | string | null = null) => {
    const base = `${path}/${resource}${suffix ? `/${suffix}` : ""}`;
    if (param) {
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
