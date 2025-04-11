import lodash from "lodash";

import {
  RESOURCE_PATHS,
  buildQueryResourceByIdURL,
  buildQueryResourceByIdsURL,
  buildQueryResourceByUserURL,
  buildSearchForResourceByLabelURL,
  buildSearchForResourceByPageURL,
} from "routes/api/endpoints/helpers";

export default {
  SERVICE: {
    SSO: {
      LOGOUT: "api/v1/svc/sso/logout",
      USER: "svc/sso/user",
    },
    LDAP: {
      SEARCH: "svc/ldap",
    },
  },
  PORTAL: {
    ANALYTICS: {
      QUERIES: `${RESOURCE_PATHS.ANALYTICS}/queries`,
      VISITS: `${RESOURCE_PATHS.ANALYTICS}/visits`,
    },
    DIRECTORY: {
      EMPLOYEE_LEVELS: buildQueryResourceByIdURL(
        RESOURCE_PATHS.DIRECTORY,
        "employee-levels"
      ),
      FUNCTIONS: buildQueryResourceByIdURL(
        RESOURCE_PATHS.DIRECTORY,
        "functions"
      ),
      RESOURCES: {
        SEARCH: (page: number | null = null, limit: number | null = null) => {
          let base = buildSearchForResourceByPageURL(
            RESOURCE_PATHS.DIRECTORY,
            "resources"
          )(page);

          if (limit) {
            if (base.match(/page/)) {
              base = `${base}&`;
            } else {
              base = `${base}?`;
            }
            base = `${base}limit=${limit}`;
          }
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
    REQUEST: {},
    USERS: {
      PROFILE: (user: string) => `${RESOURCE_PATHS.USERS}/profile?user=${user}`,
    },
  },
};
