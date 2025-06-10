import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { IStage } from "definitions/portal/request/Stage.types.ts";
import { IRole } from "definitions/portal/users/Role.types.ts";
import { IUser } from "definitions/Sso.types";

export interface IAccess {
  id: number;
  user: IUser;
  role: IRole;
  stage: IStage[] | number[];
  subfunctions: ISubFunction[] | number[];
  accessGrantedDate: Date;
  accessRevokedDate: Date | null;
}
