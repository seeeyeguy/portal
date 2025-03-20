import React from "react";

/**
 * Custom Hook to create an interval, this interval works well with functions
 * that include state changes while a normal setInterval would not.
 * @param {() => void} callback The function to call at each interval.
 * @param {number | null} delay The interval delay in milliseconds. Use null or 0 to clear the interval.
 */
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = React.useRef<() => void>();

  // Remember the latest callback.
  React.useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  React.useEffect(() => {
    function tick() {
      if (savedCallback.current) {
        savedCallback.current();
      }
    }

    // Clean up when delay is cleared, also activates when user unmounts.
    if (delay) {
      const id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}

export default useInterval;
