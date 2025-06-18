import { IResource } from "definitions/portal/directory/Resource.types.ts";
import { ITransitionGraph } from "definitions/portal/request/Transition.types.ts";
import { IAccess } from "definitions/portal/users/Access.types";

export interface IRequest {
  id: number;
  resource: IResource;
  originator: IAccess;
  status: "PENDING" | "APPROVED" | "REJECTED";
  transitions: ITransitionGraph;
  created: Date;
  modified: Date;
}
