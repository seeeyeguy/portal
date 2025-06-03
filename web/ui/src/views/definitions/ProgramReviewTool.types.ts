import { IUser } from "definitions/Sso.types";

export const DEFAULT_PORTFOLIO_ID = -1;

export enum EReviewStatus {
  SUBMITTED = -2,
  ERROR = -1,
  QUEUED = 0,
  PROCESSING = 1,
  COMPLETE = 2,
}

export interface IProgram {
  id: number;
  paNumber: string;
  name?: string;
  sector?: string;
  division?: string;
  tier?: number;
  contractValue?: number;
  activeStatus: boolean;
  created: string;
  modified: string;
  disabled: boolean;
}

export interface IPrograms {
  [key: string]: IProgram;
}

export interface IPortfolio {
  id: number;
  user?: IUser;
  programs: IPrograms;
  name: string;
  created: string;
  modified: string;
}

export interface IPortfolios {
  [key: number]: IPortfolio;
}

export interface IPortfolioMetadata {
  id: number;
  name: string;
  modified: string;
  numberOfPrograms: number;
}
