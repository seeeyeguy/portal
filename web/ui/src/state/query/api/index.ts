import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import { getCookie } from "utils/CookieUtility";

const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: `${window.location.origin}/api/v1/`,
    prepareHeaders: (headers: Headers) => {
      const multipartEndpoints = new Set(["api/v1/request/request"]);
      if (
        !headers.has("Content-Type") &&
        !multipartEndpoints.has(headers.get("Path") ?? "")
      ) {
        headers.set("Content-Type", "application/json");
      }
      headers.set("X-CSRFToken", getCookie("csrftoken"));
      return headers;
    },
  }),
  tagTypes: [
    "Access",
    "EmployeeLevel",
    "Favorite",
    "Function",
    "Portfolio",
    "Request",
    "Query",
    "QueryFilterState",
    "SubFunction",
    "Tag",
    "TagSearch",
    "Visit",
  ],
  endpoints: () => ({}),
});

export default api;
