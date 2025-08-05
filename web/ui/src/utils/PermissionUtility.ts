import { IAuthUser } from "definitions/Sso.types";

export const ROLE_LEVELS = {
  SUPERUSER: 1,
  BUSINESS_PROCESS_EXPERT: 2,
  DATA_STEWARD: 3,
};

export const RESTRICTED_ADMIN_PAGES = {
  SUPERUSER: new Set([
    "/admin/accesses",
    "/admin/employee-levels",
    "/admin/functions",
    "/admin/subfunctions",
  ]),
  BUSINESS_PROCESS_EXPERT: new Set(["/admin/approvals"]),
  DATA_STEWARD: new Set(["/admin", "/admin/tags"]),
};

/**
 * Checks if the user has the necessary Superuser permissions for the given URL path.
 *
 * @param {IAuthUser} user - The user object containing user details and accesses.
 * @param {string} urlPath - The URL path to check permissions for.
 * @returns {boolean} - Returns true if the user has the necessary Superuser permissions, otherwise false.
 */
export function hasSuperuserPermissions(
  user: IAuthUser,
  urlPath?: string
): boolean {
  if (urlPath && !RESTRICTED_ADMIN_PAGES.SUPERUSER.has(urlPath)) {
    return true;
  }

  if (!user.accesses.length) {
    return false;
  }

  return (
    user.accesses.some(
      (access) => access.role.level === ROLE_LEVELS.SUPERUSER
    ) || user.isAdmin
  );
}

/**
 * Checks if the user has the necessary Business Process Expert permissions for the given URL path.
 *
 * @param {IAuthUser} user - The user object containing user data and accesses.
 * @param {string} urlPath - The URL path to check permissions for.
 * @returns {boolean} - Returns true if the user has the necessary Business Process Expert permissions, otherwise false.
 */
export function hasNeededBusinessProcessExpertPermissions(
  user: IAuthUser,
  urlPath?: string
): boolean {
  if (urlPath && !RESTRICTED_ADMIN_PAGES.BUSINESS_PROCESS_EXPERT.has(urlPath)) {
    return true;
  }

  if (!user.accesses.length) {
    return false;
  }

  return (
    user.accesses.some(
      (access) =>
        access.role.level === ROLE_LEVELS.SUPERUSER ||
        access.role.level === ROLE_LEVELS.BUSINESS_PROCESS_EXPERT
    ) || user.isAdmin
  );
}

/**
 * Checks if the user has the necessary Data Steward permissions for the given URL path.
 *
 * @param {IAuthUser} user - The user object containing user data and accesses.
 * @param {string} urlPath - The URL path to check permissions for.
 * @returns {boolean} - Returns true if the user has the necessary Data Steward permissions, otherwise false.
 */
export function hasNeededDataStewardPermissions(
  user: IAuthUser,
  urlPath?: string
): boolean {
  if (urlPath && !RESTRICTED_ADMIN_PAGES.DATA_STEWARD.has(urlPath)) {
    return true;
  }

  if (!user.accesses.length) {
    return false;
  }

  return (
    user.accesses.some(
      (access) =>
        access.role.level === ROLE_LEVELS.SUPERUSER ||
        access.role.level === ROLE_LEVELS.BUSINESS_PROCESS_EXPERT ||
        access.role.level === ROLE_LEVELS.DATA_STEWARD
    ) || user.isAdmin
  );
}

/**
 * Evaluates the required permissions for the given URL path.
 *
 * @param {IAuthUser} user - The user object containing user data and accesses.
 * @param {string} urlPath - The URL path to check permissions for.
 * @returns {boolean} - Returns true if the user has the necessary permissions for all evaluations, otherwise false.
 */
export function requiredPermissions(user: IAuthUser, urlPath: string): boolean {
  return [
    hasSuperuserPermissions(user, urlPath),
    hasNeededBusinessProcessExpertPermissions(user, urlPath),
    hasNeededDataStewardPermissions(user, urlPath),
  ].every((permission) => permission);
}
