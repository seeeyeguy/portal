import { IAccess } from "definitions/portal/users/Access.types";

export interface IDisposition {
  id: number;
  approver: IAccess;
  disposition: "APPROVED" | "REJECTED" | "REVISE";
  justification: string;
  transition: number;
  created: Date;
}
