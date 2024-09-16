import PortalFunction from "state/types/portal/directory/Function";

export default interface SubFunction {
  id: number;
  name: string;
  description: string;
  function: PortalFunction;
  created: Date;
  modified: Date;
}
