import endpoints from "services/api";
import * as reqInit from "definitions/RequestConstants";

import * as types from "definitions/Ldap.types";

// *******************************************************************
// LDAP SEARCH SERVICE                                               *
// *******************************************************************

/**
 * Fetch employee records from LDAP search service.
 * @param {string} searchTerm email or name used to search for an employee within LDAP.
 * @param {number} offset the page offset for search results.
 * @param {number} limit the max number of results to return per request.
 * @returns {{data: types.TEmployee[], status: number}} list of employee records returned from LDAP search service in data attr.
 */
export async function searchForEmployees(
  searchTerm: string,
  offset: number = 1,
  limit: number = 10
): Promise<{ data: types.TEmployee[]; status: number }> {
  const url = `/v1/${endpoints.SERVICE.LDAP.SEARCH}`;
  const body: string = JSON.stringify({
    search_term: searchTerm,
    offset,
    limit,
  });
  const response = await fetch(url, { ...reqInit.postInit, body });
  if (!response.ok) {
    throw new Error(
      JSON.stringify({
        message: await response?.text(),
        status: response?.status,
      })
    );
  }
  const { entries }: types.TEmployeeSearchResponse = await response.json();
  if (!Array.isArray(entries)) {
    console.error(
      `Expected entries to be an array but instead got ${typeof entries}.`
    );
    return { data: [], status: response?.status };
  }
  return { data: entries, status: response?.status };
}
