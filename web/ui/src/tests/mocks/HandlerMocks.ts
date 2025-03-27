import "isomorphic-fetch";
import { http, HttpResponse } from "msw";

import endpoints from "services/api";
import * as statusCodes from "definitions/StatusCodeConstants";

const TEST_USER = {
  FIRST_NAME: "App",
  LAST_NAME: "User",
  EMAIL: "App.User@harris.com",
};

const handlers = [
  http.get(`api/v1/${endpoints.SERVICE.SSO.USER}`, () => {
    return HttpResponse.json(
      {
        email: TEST_USER.EMAIL,
        first_name: TEST_USER.FIRST_NAME,
        last_name: TEST_USER.LAST_NAME,
        is_superuser: true,
      },
      { status: statusCodes.OK }
    );
  }),
  http.get(`api/v1/${endpoints.PORTAL.DIRECTORY.EMPLOYEE_LEVELS()}`, () => {
    return HttpResponse.json([
      {
        id: 1,
        name: "Employee",
        description: "Employee Level 1.",
        created: "2024-11-14T14:45:57.059063-05:00",
        modified: "2024-11-14T14:45:57.059063-05:00",
        level: 1,
      },
      {
        id: 2,
        name: "Manager",
        description: "Manager Level 1.",
        created: "2024-11-14T14:45:57.059063-05:00",
        modified: "2024-11-14T14:45:57.059063-05:00",
        level: 2,
      },
      {
        id: 3,
        name: "Executive",
        description: "Executive Level 1.",
        created: "2024-11-14T14:45:57.059063-05:00",
        modified: "2024-11-14T14:45:57.059063-05:00",
        level: 3,
      },
    ]);
  }),
  http.get(`api/v1/${endpoints.PORTAL.DIRECTORY.FUNCTIONS()}`, () => {
    return HttpResponse.json([
      {
        id: 4,
        name: "Finance",
        description: "Finance.",
        created: "2024-11-14T14:45:57.059086-05:00",
        modified: "2024-11-14T14:45:57.059086-05:00",
      },
      {
        id: 1,
        name: "FP&A",
        description: "FP&A.",
        created: "2024-11-14T14:45:57.059086-05:00",
        modified: "2024-11-14T14:45:57.059086-05:00",
      },
      {
        id: 2,
        name: "Operations",
        description: "Operations.",
        created: "2024-11-14T14:45:57.059086-05:00",
        modified: "2024-11-14T14:45:57.059086-05:00",
      },
      {
        id: 3,
        name: "Supply Chain",
        description: "Supply Chain.",
        created: "2024-11-14T14:45:57.059086-05:00",
        modified: "2024-11-14T14:45:57.059086-05:00",
      },
    ]);
  }),
  http.post(`api/v1/${endpoints.PORTAL.DIRECTORY.RESOURCES.SEARCH()}`, () => {
    return HttpResponse.json({});
  }),
  http.get(`api/v1/${endpoints.PORTAL.DIRECTORY.TAGS.SEARCH()}`, () => {
    return HttpResponse.json([]);
  }),
  http.get(`api/v1/${endpoints.PORTAL.PREFERENCES.FAVORITES()}`, () => {
    return HttpResponse.json([]);
  }),
  http.get(
    `api/v1/${endpoints.PORTAL.PREFERENCES.QUERY_FILTER_STATE()}`,
    () => {
      return HttpResponse.json({
        id: 1,
        search: null,
        user: {
          id: 1,
          username: TEST_USER.EMAIL,
          email: TEST_USER.EMAIL,
          first_name: TEST_USER.FIRST_NAME,
          last_name: TEST_USER.LAST_NAME,
          is_active: true,
        },
        functions: [],
        employee_levels: [],
        tags: [],
        created: "2024-11-21T09:42:00.564633-05:00",
        modified: "2024-11-21T09:42:00.564653-05:00",
      });
    }
  ),
  http.get(
    `api/v1/${endpoints.PORTAL.USERS.PROFILE(TEST_USER.EMAIL).slice(0, 13)}`,
    () => {
      return HttpResponse.json({
        id: 1,
        user: {
          id: 1,
          username: TEST_USER.EMAIL,
          email: TEST_USER.EMAIL,
          first_name: TEST_USER.FIRST_NAME,
          last_name: TEST_USER.LAST_NAME,
          is_active: true,
        },
        segment: {
          id: 1,
          name: "SPACE & AIRBORNE SYSTEMS",
          description:
            "Space & Airborne Systems is a provider of mission solutions.",
        },
        uid: "618549",
        middle_initial: "M",
        unix_name: "U194879",
        job_title: "Sr Assoc, Software Engrg",
        job_function: "Engineering",
        job_family: "Software Engineering",
        job_category: "Person",
        job_level: 2,
        account_type: "Employee",
        status: "Active",
        division: "ESI",
        business_unit: "GCS",
        department: "SW-Image Processing",
        location: "FL",
        citizenship: "US",
      });
    }
  ),
];

export default handlers;
