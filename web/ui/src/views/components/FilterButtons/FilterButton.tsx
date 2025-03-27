import React from "react";
import { ToggleButton } from "adas-react-components";

import { AppDispatch, useAppDispatch } from "state/store/store";

export interface IFilterButtonProps {
  label: string;
  recordId: number;
  isActive: boolean;
  toggleAction: (recordId: number) => (dispatch: AppDispatch) => void;
}

export default function FilterButton({
  label,
  recordId,
  isActive,
  toggleAction,
}: IFilterButtonProps) {
  const dispatch = useAppDispatch();

  const onClick = React.useCallback(() => {
    dispatch(toggleAction(recordId));
  }, [recordId, dispatch, toggleAction]);

  return (
    <ToggleButton
      label={label}
      isActive={isActive}
      width={10.5}
      height={3.5}
      onClick={onClick}
    />
  );
}
