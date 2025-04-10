import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import { getCookie } from "routes/api/helpers/headers/cookies";

const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: `${window.location.origin}/api/v1/`,
    prepareHeaders: (headers: Headers) => {
      headers.set("Content-Type", "application/json");
      headers.set("X-CSRFToken", getCookie("csrftoken"));
      return headers;
    },
  }),
  tagTypes: ["Favorite", "Portfolio", "Query", "QueryFilterState", "Visit"],
  endpoints: () => ({}),
});

export default api;
