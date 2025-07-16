export const delay = (ms: number) =>
  new Promise((resolve) => setTimeout(() => resolve(true), ms));

/* eslint-disable @typescript-eslint/no-explicit-any */
export function debounce<T extends (...args: any[]) => Promise<any>>(
  func: T,
  delay: number
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let lastArgs: Parameters<T> | null = null;
  let lastPromise: Promise<ReturnType<T>> | null = null;

  return async function (...args: Parameters<T>): Promise<ReturnType<T>> {
    lastArgs = args;

    return new Promise((resolve, reject) => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }

      timeoutId = setTimeout(async () => {
        if (lastArgs) {
          try {
            lastPromise = await func(...lastArgs);
            resolve(lastPromise);
          } catch (error) {
            reject(error);
          } finally {
            timeoutId = null;
            lastArgs = null;
            lastPromise = null;
          }
        }
      }, delay);
    });
  };
}
