import employeeLevelApi, {
  useGetEmployeeLevelsQuery,
} from "state/query/api/portal/directory/EmployeeLevelApi";
import functionApi, {
  useGetFunctionsQuery,
} from "state/query/api/portal/directory/FunctionApi";
import resourceApi, {
  useSearchResourcesQuery,
} from "state/query/api/portal/directory/ResourceApi";
import subfunctionApi, {
  useGetSubFunctionsQuery,
} from "state/query/api/portal/directory/SubFunctionApi";
import tagApi, {
  useGetTagsQuery,
  useSearchTagsQuery,
} from "state/query/api/portal/directory/TagApi";

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
