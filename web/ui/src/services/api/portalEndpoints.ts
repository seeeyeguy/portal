import lodash from "lodash";

import {
  RESOURCE_PATHS,
  appendQueryParamToURL,
  buildQueryResourceByIdURL,
  buildQueryResourceByIdsURL,
  buildQueryResourceByRoleLevelsURL,
  buildQueryResourceBySubFunctionsURL,
  buildQueryResourceByUserURL,
  buildSearchForResourceByLabelURL,
  buildSearchForResourceByPageURL,
} from "services/api/portalHelpers";

const SERVER_PORT = __SERVER_PORT__;

export default {
  ANALYTICS: {
    QUERIES: (
      id: number | null = null,
      resourceId: number | null = null,
      user: string | null = null,
      page: number | null = null,
      limit: number | null = null
    ) => {
      let base = buildQueryResourceByIdURL(
        RESOURCE_PATHS.ANALYTICS,
        "queries"
      )(id);

      if (!id) {
        base = user ? appendQueryParamToURL(base, "user", user, null) : base;
        base = resourceId
          ? appendQueryParamToURL(base, "resource_id", resourceId, /user/)
          : base;
        base = page
          ? appendQueryParamToURL(base, "page", page, /user|resource_id/)
          : base;
        base = limit
          ? appendQueryParamToURL(base, "limit", limit, /user|resource_id|page/)
          : base;
      }

      return base;
    },
    VISITS: (
      id: number | null = null,
      user: string | null = null,
      resource: number | null = null,
      page: number | null = null,
      limit: number | null = null
    ) => {
      let base = buildQueryResourceByIdURL(
        RESOURCE_PATHS.ANALYTICS,
        "visits"
      )(id);

      if (!id) {
        base = user ? appendQueryParamToURL(base, "user", user, null) : base;
        base = resource
          ? appendQueryParamToURL(base, "resource", resource, /user/)
          : base;
        base = page
          ? appendQueryParamToURL(base, "page", page, /user|resource/)
          : base;
        base = limit
          ? appendQueryParamToURL(base, "limit", limit, /user|resource|page/)
          : base;
      }

      return base;
    },
  },
  DIRECTORY: {
    EMPLOYEE_LEVELS: buildQueryResourceByIdURL(
      RESOURCE_PATHS.DIRECTORY,
      "employee-levels"
    ),
    FUNCTIONS: buildQueryResourceByIdURL(RESOURCE_PATHS.DIRECTORY, "functions"),
    RESOURCES: {
      BASE: (
        id: number | null = null,
        page: number | null = null,
        limit: number | null = null
      ) => {
        let base = buildQueryResourceByIdURL(
          RESOURCE_PATHS.DIRECTORY,
          "resources"
        )(id);

        if (!id) {
          base = page ? appendQueryParamToURL(base, "page", page, null) : base;
          base = limit
            ? appendQueryParamToURL(base, "limit", limit, /page/)
            : base;
        }

        return base;
      },
      SEARCH: (page: number | null = null, limit: number | null = null) => {
        let base = buildSearchForResourceByPageURL(
          RESOURCE_PATHS.DIRECTORY,
          "resources"
        )(page);

        base = limit
          ? appendQueryParamToURL(base, "limit", limit, /page/)
          : base;

        return base;
      },
    },
    SUBFUNCTIONS: buildQueryResourceByIdURL(
      RESOURCE_PATHS.DIRECTORY,
      "subfunctions"
    ),
    TAGS: {
      BASE: buildQueryResourceByIdURL(RESOURCE_PATHS.DIRECTORY, "tags"),
      SEARCH: buildSearchForResourceByLabelURL(
        RESOURCE_PATHS.DIRECTORY,
        "tags"
      ),
    },
  },
  PREFERENCES: {
    FAVORITES: (param: number | string | null = null) => {
      const base = buildQueryResourceByIdURL(
        RESOURCE_PATHS.PREFERENCES,
        "favorites"
      )(param);

      if (lodash.isString(param)) {
        return buildQueryResourceByUserURL(
          RESOURCE_PATHS.PREFERENCES,
          "favorites"
        )(param);
      }
      return base;
    },
    QUERY_FILTER_STATE: (param: number | string | null = null) => {
      const base = buildQueryResourceByIdURL(
        RESOURCE_PATHS.PREFERENCES,
        "query-filter-state"
      )(param);

      if (lodash.isString(param)) {
        return buildQueryResourceByUserURL(
          RESOURCE_PATHS.PREFERENCES,
          "query-filter-state"
        )(param);
      }
      return base;
    },
  },
  PROGRAM_REVIEW_TOOL: {
    PORTFOLIO: (param: number | string | null = null) => {
      if (lodash.isNumber(param)) {
        return buildQueryResourceByIdURL(
          RESOURCE_PATHS.PROGRAM_REVIEW_TOOL,
          "portfolio"
        )(param);
      }
      if (lodash.isString(param)) {
        return buildQueryResourceByUserURL(
          RESOURCE_PATHS.PROGRAM_REVIEW_TOOL,
          "portfolio"
        )(param);
      }
      return `${RESOURCE_PATHS.PROGRAM_REVIEW_TOOL}/portfolio`;
    },
    PROGRAM: (param: number[]) =>
      buildQueryResourceByIdsURL(
        RESOURCE_PATHS.PROGRAM_REVIEW_TOOL,
        "program"
      )(param),
    PROGRAM_REVIEW: `${RESOURCE_PATHS.PROGRAM_REVIEW_TOOL}/program/review`,
  },
  REQUEST: {
    REQUEST: (
      id: number | null = null,
      originator: string | null = null,
      stage: number | null = null,
      status: string | null = null,
      page: number | null = null,
      limit: number | null = null,
      includeArchived: boolean | null = null
    ) => {
      let base = buildQueryResourceByIdURL(
        RESOURCE_PATHS.REQUEST,
        "request"
      )(id);

      if (!id) {
        base = originator
          ? appendQueryParamToURL(base, "originator", originator, null)
          : base;
        base = stage
          ? appendQueryParamToURL(base, "stage", stage, /originator/)
          : base;
        base = status
          ? appendQueryParamToURL(base, "status", status, /originator|stage/)
          : base;
        base = page
          ? appendQueryParamToURL(base, "page", page, /originator|stage|status/)
          : base;
        base = limit
          ? appendQueryParamToURL(
              base,
              "limit",
              limit,
              /originator|stage|status|page/
            )
          : base;
        base =
          includeArchived !== null
            ? appendQueryParamToURL(
                base,
                "include_archived",
                includeArchived,
                /originator|stage|status|page|limit/
              )
            : base;
      }

      return base;
    },
    DISPOSITION: {
      WS: `ws://${window.location.hostname}:${SERVER_PORT}/ws/disposition`,
    },
  },
  USERS: {
    ACCESS: (
      id: number | null = null,
      user: string | null = null,
      roleLevels: number[] | null = null,
      subfunctions: number[] | null = null,
      includeRevoked: boolean | null = null
    ) => {
      let base = buildQueryResourceByIdURL(RESOURCE_PATHS.USERS, "access")(id);

      if (!id) {
        let arrayParams = "";

        if (roleLevels?.length) {
          const baseWithRoleLevels = buildQueryResourceByRoleLevelsURL(
            RESOURCE_PATHS.USERS,
            "access"
          )(roleLevels);
          arrayParams = `${/\?(.*)/.exec(baseWithRoleLevels)?.[1] ?? ""}`;
        }

        if (subfunctions?.length) {
          const baseWithSubFunctions = buildQueryResourceBySubFunctionsURL(
            RESOURCE_PATHS.USERS,
            "access"
          )(subfunctions);
          arrayParams = `${arrayParams}${roleLevels ? "&" : ""}${/\?(.*)/.exec(baseWithSubFunctions)?.[1] ?? ""}`;
        }

        base = user ? appendQueryParamToURL(base, "user", user, null) : base;

        base =
          includeRevoked !== null
            ? appendQueryParamToURL(
                base,
                "include_revoked",
                includeRevoked,
                /\?user/
              )
            : base;
        base = arrayParams.length
          ? `${base}${user || includeRevoked !== null ? "&" : "?"}${arrayParams}`
          : base;
      }

      return base;
    },
    PROFILE: (user: string) => `${RESOURCE_PATHS.USERS}/profile?user=${user}`,
  },
};
