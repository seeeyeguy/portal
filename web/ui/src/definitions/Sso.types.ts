export interface IAuthAccess {
  role: { name: string; level: number };
  stages: number[];
  subfunctions: number[];
}

export interface IAuthUser {
  email: string;
  firstName: string;
  lastName: string;
  isAdmin: boolean;
  accesses: IAuthAccess[];
}
