export interface IAuthAccess {
  role: { name: string; level: number };
  stages: number[];
  subfunctions: number[];
}

export interface IAuthUser {
  username: string
  email: string;
  firstName: string;
  lastName: string;
  isAdmin: boolean;
  accesses: IAuthAccess[];
}
