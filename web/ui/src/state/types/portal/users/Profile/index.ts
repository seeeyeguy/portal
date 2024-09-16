import Segment from "state/types/portal/users/Segment";
import { User } from "state/types/services/sso";

export default interface Profile {
  user: User;
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
  segment: Segment;
  division: string;
  businessUnit: string;
  department: string;
  location: string;
  citizenship: string;
}
