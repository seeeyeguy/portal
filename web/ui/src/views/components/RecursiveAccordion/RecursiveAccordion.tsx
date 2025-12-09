import React from "react";
import { MoonLoader } from "react-spinners";
import { Transition } from "react-transition-group";
import { faAngleRight, faAngleDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";

import styles from "views/components/RecursiveAccordion/RecursiveAccordion.module.css";

const MAX_RECURSION_DEPTH = 5;

const TRANSITION_DURATION = 3000;

const TRANSITION_DEFAULT_STYLE = {
  transition: `max-height ${TRANSITION_DURATION}ms ease-out`,
  overflow: "hidden",
  maxHeight: 0,
};

const TRANSITION_STYLES = {
  entering: { maxHeight: "0rem" },
  entered: { maxHeight: "250rem" },
  exiting: { maxHeight: "250rem" },
  exited: { maxHeight: "0rem" },
};

export type AccordionContent = unknown | unknown[];

export type TransitionStates = "entering" | "entered" | "exiting" | "exited";

export interface RecursiveDataSet {
  [key: string]: AccordionContent | RecursiveDataSet;
}

export interface RecursiveAccordionProps {
  title: string;
  dataSet: RecursiveDataSet;
  recursionDepth: number;
  children: (props: unknown) => React.JSX.Element;
  isLoading?: boolean;
  className?: string;
  AccordionHeaderContent?: React.ReactElement<unknown>[];
}

export default function RecursiveAccordion({
  title,
  dataSet,
  recursionDepth,
  children,
  isLoading = false,
  className = "",
  AccordionHeaderContent = [<></>],
}: RecursiveAccordionProps) {
  const [active, setActive] = React.useState<boolean>(false);
  const nodeRef = React.useRef(null);

  const computedClassName = React.useMemo(
    () =>
      !(recursionDepth % 2)
        ? styles["recursive-accordion-even"]
        : styles["recursive-accordion-odd"],
    [recursionDepth]
  );

  const toggleAccordion = React.useCallback(() => {
    setActive((state) => !state);
  }, [setActive]);

  if (recursionDepth > MAX_RECURSION_DEPTH) {
    return <p>Max Level Exceeded...</p>;
  }

  const size = Object.keys(dataSet).length;

  return (
    <details
      className={`${className} ${styles["recursive-accordion"]} ${computedClassName}`}
      aria-level={recursionDepth}
    >
      <summary onClick={toggleAccordion} role="button">
        <div
          className={styles["accordion-header"]}
          aria-description={`${title} accordion header`}
          data-testid={active ? "accordion-active" : "accordion-inactive"}
        >
          {title.toUpperCase()}
        </div>
        <div
          className={styles["accordion-header-content"]}
          aria-description={`${title} accordion header content`}
        >
          {AccordionHeaderContent[recursionDepth]}
          <>{recursionDepth > 0 && <>{size}</>}</>
        </div>
        <div
          aria-checked={active}
          aria-description={`${title} accordion header arrow marker`}
        >
          {active ? (
            <FontAwesomeIcon icon={faAngleDown} />
          ) : (
            <FontAwesomeIcon icon={faAngleRight} />
          )}
        </div>
      </summary>
      <Transition nodeRef={nodeRef} in={active} timeout={100}>
        {(state) => (
          <section
            ref={nodeRef}
            style={{
              ...TRANSITION_DEFAULT_STYLE,
              ...TRANSITION_STYLES[state as TransitionStates],
            }}
          >
            {isLoading && (
              <div
                className={
                  styles["recursive-accordion-loading-spinner-container"]
                }
              >
                <MoonLoader />
              </div>
            )}
            {!isLoading &&
              (!React.isValidElement(dataSet) && lodash.isPlainObject(dataSet)
                ? lodash
                    .keys(dataSet)
                    .map((key, index) => (
                      <RecursiveAccordion
                        title={key}
                        dataSet={dataSet[key] as RecursiveDataSet}
                        recursionDepth={recursionDepth + 1}
                        children={children}
                        AccordionHeaderContent={AccordionHeaderContent}
                        key={index}
                      />
                    ))
                : children({ dataSet }))}
          </section>
        )}
      </Transition>
    </details>
  );
}
