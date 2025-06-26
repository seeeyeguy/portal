import { IAuthAccess, IAuthUser } from "definitions/Sso.types";

interface ApiAuthAccess extends IAuthAccess {}

export interface ApiAuthUser {
  email: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
  accesses?: ApiAuthAccess[];
}

export function transformApiAuthUser(data: ApiAuthUser): IAuthUser {
  return {
    email: data.email,
    firstName: data.first_name,
    lastName: data.last_name,
    isAdmin: data.is_superuser,
    accesses: data?.accesses ?? [],
  };
}
