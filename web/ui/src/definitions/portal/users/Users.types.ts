import { IUser } from "definitions/Sso.types";

export interface ISegment {
  id: number;
  name: string;
  description: string;
}
export interface IProfile {
  user: IUser;
  uid: string;
  middleInitial: string;
  unixName: string;
  jobTitle: string;
  jobFunction: string;
  jobFamily: string;
  jobCategory: string;
  jobLevel: number;
  accountType: string;
  status: string;
  segment: ISegment;
  division: string;
  businessUnit: string;
  department: string;
  location: string;
  citizenship: string;
}
