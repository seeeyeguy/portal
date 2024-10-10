export interface SearchQuery {
  term: string;
  record: number | null;
}

export interface SearchParams {
  search: SearchQuery;
  employeeLevels: number[];
  functions: number[];
  tags: number[];
}
