import FilterButton from "components/buttons/FilterButton";

import { FilterButtonsProps } from "components/buttons/FilterButtons/types";

import styles from "components/buttons/FilterButtons/styles/index.module.css";

export default function FilterButtons({
  title,
  records,
  activeFilters,
  toggleAction,
}: FilterButtonsProps) {
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
