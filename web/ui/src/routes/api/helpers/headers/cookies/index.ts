import { inTest } from "utils/constants/environments";

type Cookies = { [key: string]: string };

export function getCookies() {
  if (!document?.cookie) {
    throw new Error("No Cookies have been set.");
  }
  const cookiesKeyValuePairs = document?.cookie?.split("; ");
  const Cookies = cookiesKeyValuePairs
    .map((pair) => pair.split("="))
    .reduce((acc: Cookies, item: string[]) => {
      acc[item[0].trim()] = item[1];
      return acc;
    }, {});
  return Cookies;
}

export function getCookie(cookie: string) {
  try {
    const cookies = getCookies();
    if (!(cookie in cookies)) {
      throw new Error(`${cookie} not in cookies`);
    }
    return cookies[cookie];
  } catch (error) {
    if (!inTest()) {
      console.error(error);
    }
    return "";
  }
}
