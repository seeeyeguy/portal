import "isomorphic-fetch";
import { http, HttpResponse } from "msw";

import endpoints from "routes/api/endpoints";
import * as statusCodes from "routes/api/helpers/headers/status-codes";

const handlers = [
  http.get(`api/v1/${endpoints.SERVICE.SSO.USER}`, () => {
    return HttpResponse.json(
      {
        email: "App.User@harris.com",
        first_name: "App",
        last_name: "User",
        is_superuser: true,
      },
      { status: statusCodes.OK }
    );
  }),
];

export default handlers;
