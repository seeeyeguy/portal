/**
 * Convert a number of seconds to a readable string.
 * @param number The number in seconds to convert.
 * @returns Returns a string including up to two largest non‑zero units (e.g. "3 days 2 hours", "30 minutes").
 */
export const formatSeconds = (seconds: number): string => {
    const units: [string, number][] = [
      ["day", 86400],
      ["hour", 3600],
      ["minute", 60],
      ["second", 1],
    ];
  
    const parts: string[] = [];
  
    for (const [name, size] of units) {
      const value = Math.floor(seconds / size);
      if (value > 0) {
        parts.push(`${value} ${name}${value > 1 ? "s" : ""}`);
        seconds -= value * size;
      }
      if (parts.length === 2) break; // limit to two increments.
    }
  
    // If the timeout is 0 (unlikely) fall back to "0 seconds".
    return parts.length ? parts.join(" ") : "0 seconds";
  };