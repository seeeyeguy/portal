import EmployeeLevel from "state/types/portal/directory/EmployeeLevel";
import SubFunction from "state/types/portal/directory/SubFunction";
import Tag from "state/types/portal/directory/Tag";

interface Restricted {
  [key: string]: string[];
}

export default interface Resource {
  id: number;
  uid: string;
  previousRevision: number;
  revisionNumber: number;
  name: string;
  description: string;
  url: string;
  thumbnail: string;
  primaryPointOfContact: string;
  employeeLevels: EmployeeLevel[];
  subfunctions: SubFunction[];
  tags: Tag[];
  type: string;
  download: boolean;
  active: boolean;
  created: Date;
  favoritedBy: string[];
  restricted?: Restricted;
  site: string[];
}

export interface ResourceFunctree {
  [key: string]: Resource[] | ResourceFunctree;
}

export type ResourceRecords = ResourceFunctree | Resource[];
