import { transformApiUser as transformUserRecord } from "routes/api/helpers/transforms/services/sso";

export interface ApiUser {
  email: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
}

export default transformUserRecord;
