import Program from "state/types/program_review_tool/Program";
import { IUser } from "definitions/Sso.types";

export default interface Portfolio {
  id: number;
  user: IUser;
  programs: Program[];
  name: string;
  created: Date;
  modified: Date;
}
