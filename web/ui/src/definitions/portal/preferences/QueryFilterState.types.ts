import { IQuery } from "definitions/portal/Analytics.types";
import { IUser } from "definitions/portal/users/User.types";

export interface IQueryFilterState {
  id: number;
  search: IQuery;
  user: IUser;
  functions: number[];
  employeeLevels: number[];
  tags: number[];
}
