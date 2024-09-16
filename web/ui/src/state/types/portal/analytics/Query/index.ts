import Resource from "state/types/portal/directory/Resource";
import { User } from "state/types/services/sso";

export default interface Query {
  id: number;
  user: User;
  searchTerm: string;
  resources?: Resource[];
  created: Date;
}
