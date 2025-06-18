import lodash from "lodash";

import {
  IApiResource,
  transformResourceRecord,
} from "state/query/api/portal/directory/ResourceHelper";
import {
  IApiTransitionGraph,
  transformTransitionRecord,
} from "state/query/api/portal/request/TransitionHelper";
import {
  IApiAccess,
  transformAccessRecord,
} from "state/query/api/portal/users/AccessHelper";

import { IRequest } from "definitions/portal/request/Request.types";

export interface IApiRequest {
  id: number;
  resource: IApiResource;
  originator: IApiAccess;
  status: string;
  transitions: IApiTransitionGraph;
  created: Date;
  modified: Date;
}

/**
 * Transforms a `portal.request.Request` record from snake_casing
 * to camelCasing.
 * @param data A `portal.request.Request` record.
 * @returns A `portal.request.Request` record with desired casing.
 */
export function transformRequestRecord(data: IApiRequest): IRequest {
  const transitions = {
    ...data.transitions,
    nodes: Object.entries(data.transitions.nodes ?? {}).reduce(
      (acc, [key, node]) => {
        const k = lodash.toNumber(key);
        const v = transformTransitionRecord(node);
        return {
          ...acc,
          [k]: v,
        };
      },
      {}
    ),
  };
  return {
    ...data,
    resource: transformResourceRecord(data.resource),
    originator: transformAccessRecord(data.originator),
    transitions,
  } as unknown as IRequest;
}
