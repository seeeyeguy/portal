import { IResource } from "definitions/portal/directory/Resource.types";
import { IUser } from "definitions/Sso.types";

export interface IQuery {
  id: number;
  user: IUser;
  searchTerm: string;
  resources?: IResource[];
  created: Date;
}

export interface IVisit {
  id: number;
  user: IUser;
  resource: IResource;
  created: Date;
}
