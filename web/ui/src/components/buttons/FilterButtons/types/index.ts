import { AppDispatch } from "state/store";

interface Record {
  id: number;
  name: string;
}

export interface FilterButtonsProps {
  title: string;
  records: Record[];
  activeFilters: number[];
  toggleAction: (recordId: number) => (dispatch: AppDispatch) => void;
}
