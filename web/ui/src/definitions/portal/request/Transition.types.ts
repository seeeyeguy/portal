import { IDisposition } from "definitions/portal/request/Disposition.types.ts";
import { IStage } from "definitions/portal/request/Stage.types.ts";

export interface ITransition {
  id: number;
  request: number;
  stage: IStage;
  previousTransition: number | null;
  dispositions?: IDisposition[] | number[];
  created: Date;
}

interface ITransitionNode {
  [key: number]: ITransition;
}

export interface ITransitionGraph {
  latest: number;
  nodes: ITransitionNode;
}
