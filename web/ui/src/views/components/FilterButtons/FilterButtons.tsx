import FilterButton from "views/components/FilterButtons/FilterButton";

import { AppDispatch } from "state/store/store";

import styles from "views/components/FilterButtons/FilterButtons.module.css";

interface Record {
  id: number;
  name: string;
}

export interface IFilterButtonsProps {
  title: string;
  records: Record[];
  activeFilters: number[];
  toggleAction: (recordId: number) => (dispatch: AppDispatch) => void;
}

export default function FilterButtons({
  title,
  records,
  activeFilters,
  toggleAction,
}: IFilterButtonsProps) {
  return (
    <div
      className={styles["filter-buttons-row"]}
      aria-description={`${title} filter buttons row`}
    >
      <header>
        <h2>{title}</h2>
      </header>
      <div
        className={styles["filter-buttons-container"]}
        aria-description="container for buttons"
      >
        {records.map((record, index) => (
          <FilterButton
            label={record.name}
            recordId={record.id}
            isActive={activeFilters.includes(record.id)}
            toggleAction={toggleAction}
            key={index}
          />
        ))}
      </div>
    </div>
  );
}
