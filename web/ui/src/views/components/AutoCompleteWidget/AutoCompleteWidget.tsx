import React from "react";
import {
  AutoComplete,
  AutoCompleteCompleteEvent,
} from "primereact/autocomplete";
import { WidgetProps } from "@rjsf/utils";

import styles from "views/components/AutoCompleteWidget/AutoCompleteWidget.module.css";

/**
 * AutoCompleteWidget component for React JSON Schema Form.
 * This widget uses PrimeReact's AutoComplete component.
 *
 * @param {AutoCompleteWidgetProps} props - The properties passed to the widget.
 * @returns {JSX.Element} The rendered AutoCompleteWidget component.
 */
export default function AutoCompleteWidget({
  value,
  options,
  disabled,
  onChange,
}: WidgetProps) {
  // Destructure options to avoid passing invalid options to the DOM element.
  const {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    enumOptions: _,
    field: field,
    completeMethod,
    ...restOptions
  } = options || {};

  const [filteredSuggestions, setFilteredSuggestions] = React.useState<
    string[]
  >([]);

  const handleComplete = (event: AutoCompleteCompleteEvent) => {
    if (completeMethod) {
      completeMethod(event.query).then((results: string[]) => {
        setFilteredSuggestions(results);
      });
    }
  };

  return (
    <AutoComplete
      value={value}
      suggestions={filteredSuggestions}
      disabled={disabled}
      field={field as string}
      completeMethod={handleComplete}
      onChange={(e) => onChange(e.value)}
      dropdown
      showEmptyMessage={true}
      className={styles["autocomplete-widget"]}
      {...restOptions}
    />
  );
}
