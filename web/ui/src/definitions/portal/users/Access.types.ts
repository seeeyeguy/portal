import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { IStage } from "definitions/portal/request/Stage.types";
import { IRole } from "definitions/portal/users/Role.types";
import { IUser } from "definitions/portal/users/User.types";

export interface IAccess {
  id: number;
  user: IUser;
  role: IRole;
  stage: IStage[] | number[];
  subfunctions: ISubFunction[] | number[];
  accessGrantedDate: Date;
  accessRevokedDate: Date | null;
}
