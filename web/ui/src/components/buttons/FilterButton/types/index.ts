import { AppDispatch } from "state/store";

export interface FilterButtonProps {
  label: string;
  recordId: number;
  isActive: boolean;
  toggleAction: (recordId: number) => (dispatch: AppDispatch) => void;
}
