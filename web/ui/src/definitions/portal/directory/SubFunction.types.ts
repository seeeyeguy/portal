import { IFunction } from "definitions/portal/directory/Function.types";

export interface ISubFunction {
  id: number;
  name: string;
  description: string;
  function: IFunction;
  created: Date;
  modified: Date;
}
