import { IResource } from "definitions/portal/directory/Resource.types";
import { IUser } from "definitions/portal/users/User.types";

export interface IFavorite {
  id: number;
  user: IUser;
  resource: IResource;
  rank: number;
  created: Date;
}
