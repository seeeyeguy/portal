import Query from "state/types/portal/analytics/Query";
import { User } from "state/types/services/sso";

export default interface QueryFilterState {
  id: number;
  search: Query;
  user: User;
  functions: number[];
  employeeLevels: number[];
  tags: number[];
}
