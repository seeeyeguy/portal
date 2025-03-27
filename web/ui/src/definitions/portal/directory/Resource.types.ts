import { IEmployeeLevel } from "definitions/portal/directory/EmployeeLevel.types";
import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { ITag } from "definitions/portal/directory/Tag.types";

interface IRestricted {
  [key: string]: string[];
}

export interface IResource {
  id: number;
  uid: string;
  previousRevision: number;
  revisionNumber: number;
  name: string;
  description: string;
  url: string;
  thumbnail: string;
  primaryPointOfContact: string;
  employeeLevels: IEmployeeLevel[];
  subfunctions: ISubFunction[];
  tags: ITag[];
  type: string;
  download: boolean;
  active: boolean;
  created: Date;
  favoritedBy: string[];
  restricted?: IRestricted;
  site: string[];
}

export interface IResourceFunctree {
  [key: string]: IResource[] | IResourceFunctree;
}

export type TResourceRecords = IResourceFunctree | IResource[];

export interface ISearchQuery {
  term: string;
  record: number | null;
}

export interface ISearchParams {
  search: ISearchQuery;
  employeeLevels: number[];
  functions: number[];
  tags: number[];
}
