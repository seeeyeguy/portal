export type Employee = {
  email: string;
  unixName?: string;
  uid?: string;
  firstName: string;
  middleInitial?: string;
  lastName: string;
  location?: string;
  title: string;
  level?: number;
  citizenship: string;
  accountType?: string;
  employeeStatus?: string;
  segment: string;
  department?: string;
  jobFamily?: string;
  jobFunction?: string;
  division?: string;
  jobCategory?: string;
  businessUnit?: string;
};

export type EmployeeSearchRequestBody = {
  searchTerm: string;
  attributes?: string;
  matchWholeWord?: boolean;
  offset?: number;
  limit?: number;
  content_count?: number;
};

export type EmployeeSearchResponse = {
  entries: Employee[];
  result: {
    code: number;
    description: string;
  };
  contentCount?: number;
};
