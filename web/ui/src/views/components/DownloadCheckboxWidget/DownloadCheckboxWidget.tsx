import React from "react";
import { Checkbox } from "primereact/checkbox";
import { WidgetProps } from "@rjsf/utils";
import { Tooltip } from "primereact/tooltip";

import styles from "views/components/DownloadCheckboxWidget/DownloadCheckboxWidget.module.css";

/**
 * DownloadCheckboxWidget component for React JSON Schema Form.
 * This widget uses PrimeReact's Checkbox and Tooltip components.
 *
 * @param {DownloadCheckboxWidgetProps} props - The properties passed to the widget.
 * @returns {JSX.Element} The rendered DownloadCheckboxWidget component.
 */
export default function DownloadCheckboxWidget({
  value,
  onChange,
}: WidgetProps) {
  const containerRef = React.useRef(null);
  return (
    <div>
      <Tooltip
        target={containerRef}
        content="Provide downloadable content."
        position="top"
      />

      <div ref={containerRef} className={styles["download-checkbox"]}>
        <Checkbox
          inputId="myCheckbox"
          checked={!!value}
          onChange={(e) => onChange(e.checked)}
        />
        <label htmlFor="myCheckbox" className="ml-2">
          Download
        </label>
      </div>
    </div>
  );
}
