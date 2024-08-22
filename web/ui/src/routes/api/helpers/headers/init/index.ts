import { getCookie } from "routes/api/helpers/headers/cookies";

// REQUEST METHODS
export const GET = "GET";
export const POST = "POST";
export const PUT = "PUT";
export const PATCH = "PATCH";
export const DELETE = "DELETE";

// REQUEST OPTIONS
export const headers = {
  Accept: "application/json",
  "Content-Type": "application/json",
  "X-CSRFToken": getCookie("csrftoken"),
};
export const getInit = { method: GET, headers };
export const postInit = { method: POST, headers };
export const putInit = { method: PUT, headers };
export const patchInit = { method: PATCH, headers };
export const deleteInit = { method: DELETE, headers };
