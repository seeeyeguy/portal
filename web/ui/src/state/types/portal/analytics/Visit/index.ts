import Resource from "state/types/portal/directory/Resource";
import { User } from "state/types/services/sso";

export default interface Visit {
  id: number;
  user: User;
  resource: Resource;
  created: Date;
}
