import { redirect } from "react-router-dom";

import { REDIRECT } from "routes/api/helpers/headers/status-codes";
import authApi from "state/query/api/auth";
import store from "state/store";

/**
 * Redirect user to login, or load user data.
 * @returns {Promise}
 */
export async function login() {
  const promise = store.dispatch(
    authApi.endpoints.getAuthenticatedUser.initiate()
  );
  const response = await promise;
  if (response.isError && "status" in response.error && response.error.status === REDIRECT) {
    if("data" in response.error){
      return redirect(response.error.data as string);
    } 
  }
  return response?.data?.data;
}
