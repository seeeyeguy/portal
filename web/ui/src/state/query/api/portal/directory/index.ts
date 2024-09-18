import employeeLevelApi, {
  useGetEmployeeLevelsQuery,
} from "state/query/api/portal/directory/EmployeeLevel";
import functionApi, {
  useGetFunctionsQuery,
} from "state/query/api/portal/directory/Function";
import resourceApi, {
  useSearchResourcesQuery,
} from "state/query/api/portal/directory/Resource";
import subfunctionApi, {
  useGetSubFunctionsQuery,
} from "state/query/api/portal/directory/SubFunction";
import tagApi, {
  useGetTagsQuery,
  useSearchTagsQuery,
} from "state/query/api/portal/directory/Tag";

export default {
  employeeLevelApi,
  functionApi,
  resourceApi,
  subfunctionApi,
  tagApi,
  useGetEmployeeLevelsQuery,
  useGetFunctionsQuery,
  useSearchResourcesQuery,
  useGetSubFunctionsQuery,
  useGetTagsQuery,
  useSearchTagsQuery,
};
