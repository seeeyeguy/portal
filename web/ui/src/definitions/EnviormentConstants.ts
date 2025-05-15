export const DEVELOPMENT = "development";
export const TEST = "test";

export function inDevelopment() {
  return process.env.NODE_ENV === DEVELOPMENT;
}

export function inTest() {
  return process.env.NODE_ENV === TEST;
}
