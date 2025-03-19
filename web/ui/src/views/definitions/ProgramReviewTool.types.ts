export interface IProgram {
  id: string;
  paNumber: string;
  programName?: string;
  sector?: string;
  division?: string;
  tier?: number;
  contractValue?: string;
  valid: boolean;
  disabled: boolean;
}

export interface IPrograms {
  [key: string]: IProgram;
}

export interface IPortfolio {
  id: string;
  user: string;
  programs: IPrograms;
  name: string;
  created: string;
  modified: string;
}

export interface IPortfolios {
  [key: string]: IPortfolio;
}
