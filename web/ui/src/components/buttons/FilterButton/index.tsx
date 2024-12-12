import React from "react";
import { ToggleButton } from "adas-react-components";

import { FilterButtonProps } from "components/buttons/FilterButton/types";

import { useAppDispatch } from "state/store";

export default function FilterButton({
  label,
  recordId,
  isActive,
  toggleAction,
}: FilterButtonProps) {
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
