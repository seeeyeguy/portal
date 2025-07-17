import { WidgetProps } from "@rjsf/utils";

import {
  InputNumber,
  InputNumberValueChangeEvent,
} from "primereact/inputnumber";

/** Properties for the UpDownWidget component. */
export interface UpDownWidgetProps extends WidgetProps {
  /** Extended options allowing numbers to be automatically skipped in the input. */
  options: { skipNumbers?: number[] };
}

/**
 * UpDownWidget component for React JSON Schema Form.
 * This widget uses PrimeReact's InputNumber component and skips specified numbers.
 *
 * @param {WidgetProps} props - The properties passed to the widget.
 * @returns {JSX.Element} The rendered UpDownWidget component.
 */
export default function UpDownWidget({
  value,
  options,
  disabled,
  onChange,
}: WidgetProps) {
  // Destructure options to avoid passing invalid options to the DOM element.
  const {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    enumOptions: _,
    skipNumbers,
    min,
    max,
    ...restOptions
  } = options || {};

  // Skip numbers that that exist in the skipNumbers option array.
  const handleChange = (event: InputNumberValueChangeEvent) => {
    let newValue = event.value as number;
    while (skipNumbers?.includes(newValue)) {
      newValue = newValue > (value as number) ? newValue + 1 : newValue - 1;
    }
    onChange(newValue);
  };

  return (
    <InputNumber
      value={value}
      min={min}
      max={max}
      onValueChange={handleChange}
      showButtons
      inputStyle={{ pointerEvents: "none" }}
      disabled={disabled}
      {...restOptions}
    />
  );
}
