export default interface Program {
  id: number;
  paNumber: string;
  name: string;
  segment: string;
  sector: string;
  division: string;
  tier: number;
  contractValue: number;
  activeStatus: boolean;
  created: Date;
  modified: Date;
}
