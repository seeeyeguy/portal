import Resource from "state/types/portal/directory/Resource";
import { User } from "state/types/services/sso";

export default interface Favorite {
  id: number;
  user: User;
  resource: Resource;
  rank: number;
  created: Date;
}
