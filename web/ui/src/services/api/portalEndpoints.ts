import lodash from "lodash";

import {
  RESOURCE_PATHS,
  appendQueryParamToURL,
  buildQueryResourceByIdURL,
  buildQueryResourceByIdsURL,
  buildQueryResourceByPANumberURL,
  buildQueryResourceByPANumbersURL,
  buildQueryResourceByRoleLevelsURL,
  buildQueryResourceByStagesURL,
  buildQueryResourceBySubFunctionsURL,
  buildQueryResourceByTiersURL,
  buildQueryResourceByUserURL,
  buildSearchForResourceByLabelURL,
  buildSearchForResourceByPageURL,
} from "services/api/portalHelpers";

const SCHEME = __SCHEME__;
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
        base = appendQueryParamToURL(base, "user", user);
        base = appendQueryParamToURL(base, "resource_id", resourceId);
        base = appendQueryParamToURL(base, "page", page);
        base = appendQueryParamToURL(base, "limit", limit);
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
        base = appendQueryParamToURL(base, "user", user);
        base = appendQueryParamToURL(base, "resource", resource);
        base = appendQueryParamToURL(base, "page", page);
        base = appendQueryParamToURL(base, "limit", limit);
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
          base = appendQueryParamToURL(base, "page", page);
          base = appendQueryParamToURL(base, "limit", limit);
        }

        return base;
      },
      SEARCH: (page: number | null = null, limit: number | null = null) => {
        let base = buildSearchForResourceByPageURL(
          RESOURCE_PATHS.DIRECTORY,
          "resources"
        )(page);

        base = appendQueryParamToURL(base, "limit", limit);

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
    PROGRAM: (
      ids: number[] | null = null,
      paNumbers: string[] | null = null,
      programMember: string | null = null,
      tiers: number[] | null = null,
      activeOnly: boolean | null = null,
      page: number | null = null,
      limit: number | null = null
    ) => {
      let base = buildQueryResourceByIdsURL(
        RESOURCE_PATHS.PROGRAM_REVIEW_TOOL,
        "program"
      )(ids);

      if (paNumbers?.length) {
        base = buildQueryResourceByPANumbersURL(
          RESOURCE_PATHS.PROGRAM_REVIEW_TOOL,
          "program"
        )(paNumbers);
      }

      let arrayParams = "";
      if (tiers?.length) {
        const baseWithTiers = buildQueryResourceByTiersURL(
          RESOURCE_PATHS.PROGRAM_REVIEW_TOOL,
          "program"
        )(tiers);
        arrayParams = `${/\?(.*)/.exec(baseWithTiers)?.[1] ?? ""}`;
      }

      base = appendQueryParamToURL(base, "program_member", programMember);
      base = appendQueryParamToURL(base, "active_only", activeOnly);
      base = appendQueryParamToURL(base, "page", page);
      base = appendQueryParamToURL(base, "limit", limit);

      base = arrayParams.length
        ? `${base}${/\?(.*?)=/.test(base) ? "&" : "?"}${arrayParams}`
        : base;

      return base;
    },
    PROGRAM_REVIEW: `${RESOURCE_PATHS.PROGRAM_REVIEW_TOOL}/program/review`,
    RECORD: (
      paNumber: string | null = null,
      reportingPeriod: number | null = null,
      refresh: boolean | null = null
    ) => {
      let base = buildQueryResourceByPANumberURL(
        RESOURCE_PATHS.PROGRAM_REVIEW_TOOL,
        "record"
      )(paNumber);
      base = appendQueryParamToURL(base, "reporting_period", reportingPeriod);
      base = appendQueryParamToURL(base, "refresh", refresh);
      return base;
    },
    REPORTING_PERIOD: (previousPeriodCount: number | null = null) => {
      let base = `${RESOURCE_PATHS.PROGRAM_REVIEW_TOOL}/reporting-period`;
      base = appendQueryParamToURL(
        base,
        "previous_period_count",
        previousPeriodCount
      );
      return base;
    },
  },
  REQUEST: {
    REQUEST: (
      id: number | null = null,
      originator: string | null = null,
      stages: number[] | null = null,
      subfunctions: number[] | null = null,
      status: string | null = null,
      page: number | null = null,
      limit: number | null = null,
      includeArchived: boolean | null = null,
      deleted: boolean | null = null,
    ) => {
      let base = buildQueryResourceByIdURL(
        RESOURCE_PATHS.REQUEST,
        "request"
      )(id);

      if (!id) {
        let arrayParams = "";

        if (stages?.length) {
          const baseWithStages = buildQueryResourceByStagesURL(
            RESOURCE_PATHS.REQUEST,
            "request"
          )(stages);
          arrayParams = `${/\?(.*)/.exec(baseWithStages)?.[1] ?? ""}`;
        }

        if (subfunctions?.length) {
          const baseWithSubFunctions = buildQueryResourceBySubFunctionsURL(
            RESOURCE_PATHS.REQUEST,
            "request"
          )(subfunctions);
          arrayParams = `${arrayParams}${stages ? "&" : ""}${/\?(.*)/.exec(baseWithSubFunctions)?.[1] ?? ""}`;
        }

        base = appendQueryParamToURL(base, "originator", originator);
        base = appendQueryParamToURL(base, "status", status);
        base = appendQueryParamToURL(base, "page", page);
        base = appendQueryParamToURL(base, "limit", limit);
        base = appendQueryParamToURL(
          base,
          "include_archived",
          includeArchived,
          /originator|stage|status|page|limit/
        );
        base = appendQueryParamToURL(base, "deleted", deleted);
        base = arrayParams.length
          ? `${base}${/\?(.*?)=/.test(base) ? "&" : "?"}${arrayParams}`
          : base;
      }

      return base;
    },
    REQUEST_NOTIFICATION: {
      WS: SCHEME?.endsWith("s")
        ? "ws/request-notification"
        : `ws://${window.location.hostname}:${SERVER_PORT}/ws/request-notification`,
    },
    DISPOSITION: {
      WS: SCHEME?.endsWith("s")
        ? "/ws/disposition"
        : `ws://${window.location.hostname}:${SERVER_PORT}/ws/disposition`,
    },
  },
  USERS: {
    ACCESS: (
      id: number | null = null,
      ids: number[] | null = null,
      user: string | null = null,
      roleLevels: number[] | null = null,
      subfunctions: number[] | null = null,
      includeRevoked: boolean | null = null,
      addSubdomain: boolean = false
    ) => {
      let base = buildQueryResourceByIdURL(
        RESOURCE_PATHS.USERS,
        !addSubdomain ? "access" : "access/subfunctions"
      )(id);

      if (ids?.length) {
        base = buildQueryResourceByIdsURL(
          RESOURCE_PATHS.USERS,
          !addSubdomain ? "access" : "access/subfunctions"
        )(ids);
      }

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

        base = appendQueryParamToURL(base, "user", user);
        base = appendQueryParamToURL(
          base,
          "include_revoked",
          includeRevoked,
          /\?user/
        );

        base = arrayParams.length
          ? `${base}${/\?(.*?)=/.test(base) ? "&" : "?"}${arrayParams}`
          : base;
      }

      return base;
    },
    PROFILE: (user: string) => `${RESOURCE_PATHS.USERS}/profile?user=${user}`,
  },
};
