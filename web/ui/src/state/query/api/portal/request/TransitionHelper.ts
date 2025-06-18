import { IApiDisposition } from "state/query/api/portal/request/DispositionHelper";
import { IApiStage } from "state/query/api/portal/request/StageHelper";

import { ITransition } from "definitions/portal/request/Transition.types";

import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";

export interface IApiTransition {
  id: number;
  request: number;
  stage: IApiStage;
  previous_revision: number;
  disposition: IApiDisposition | number[];
  created: Date;
}

interface IApiTransitionNode {
  [key: string]: IApiTransition;
}

export interface IApiTransitionGraph {
  latest: number;
  nodes: IApiTransitionNode;
}

/**
 * Transforms a `portal.request.Transition` record from snake_casing
 * to camelCasing.
 * @param data A `portal.request.Transition` record.
 * @returns A `portal.request.Transition` record with desired casing.
 */
export function transformTransitionRecord(data: IApiTransition): ITransition {
  return snakeCaseToCamelCase({ ...data }) as unknown as ITransition;
}
