import { IQuery } from "definitions/portal/Analytics.types";
import { IUser } from "definitions/Sso.types";

export interface IQueryFilterState {
  id: number;
  search: IQuery;
  user: IUser;
  functions: number[];
  employeeLevels: number[];
  tags: number[];
}
