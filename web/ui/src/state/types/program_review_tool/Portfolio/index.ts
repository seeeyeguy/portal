import Program from "state/types/program_review_tool/Program";
import { User } from "state/types/services/sso";

export default interface Portfolio {
  id: number;
  user: User;
  programs: Program[];
  name: string;
  created: Date;
  modified: Date;
}
