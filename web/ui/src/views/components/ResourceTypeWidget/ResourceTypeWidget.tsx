import { Dropdown, DropdownChangeEvent } from "primereact/dropdown";
import { WidgetProps } from "@rjsf/utils";

import styles from "views/components/ResourceTypeWidget/ResourceTypeWidget.module.css";

import { resourceTypeThumbnailPaths } from "views/utils/ResourceLinksUtility";

/**
 * ResoureTypeWidget component for React JSON Schema Form.
 * This widget uses PrimeReact's Dropdown component.
 *
 * @param {ResourceTypeWidgetProps} props - The properties passed to the widget.
 * @returns {JSX.Element} The rendered ResoureTypeWidget component.
 */
export default function ResourceTypeWidget({
  value,
  options,
  disabled,
  onChange,
}: WidgetProps) {
  const resourceTypes = (options.enumOptions ?? []) as {
    label: string;
    value: string;
  }[];

  const handleTypeChange = (event: DropdownChangeEvent) => {
    onChange(event.value || null);
  };

  // Layout for the value that is selected
  const selectedResourceTypeTemplate = (option: {
    label: string;
    value: string;
  }) => {
    if (option) {
      const imagePath =
        "/thumbnail/resourceTypes/" + resourceTypeThumbnailPaths[option.value];
      return (
        <>
          <img src={imagePath} alt={option.label} />
          <span>{option.label}</span>
        </>
      );
    }
    return <span>Select Resource Type</span>;
  };

  // Layout for the options when Dropdown is expanded
  const resourceTypeOptionsTemplate = (option: {
    label: string;
    value: string;
  }) => {
    if (option) {
      const imagePath =
        "/thumbnail/resourceTypes/" + resourceTypeThumbnailPaths[option.value];
      return (
        <>
          <img src={imagePath} alt={option.label} />
          <span>{option.label}</span>
        </>
      );
    }
    return <span>Select Resource Type</span>;
  };

  return (
    <div
      className={styles["type-selection"]}
      aria-description="container for resource types"
    >
      <Dropdown
        appendTo="self"
        disabled={disabled}
        value={value}
        options={resourceTypes}
        optionLabel="label"
        optionValue="value"
        itemTemplate={resourceTypeOptionsTemplate}
        valueTemplate={selectedResourceTypeTemplate}
        onChange={handleTypeChange}
        placeholder="Select Resource Type"
        tooltip="Source where content may be viewed"
        tooltipOptions={{ position: "top" }}
      />
    </div>
  );
}
