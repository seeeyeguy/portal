import lodash from "lodash";

import { camelCaseToSnakeCase } from "utils/transforms/helpers";

describe("Test `camelCaseToSnakeCase` transform function", () => {
  test("Transform array of objects", () => {
    const data = [{ snakeCaseKey: [{ snakeCaseKey: 1 }] }];
    const expected = [{ snake_case_key: [{ snake_case_key: 1 }] }];
    expect(lodash.isEqual(camelCaseToSnakeCase(data), expected)).toBeTruthy();
  });
  test("Transform object of objects", () => {
    const data = {
      snakeCaseKey: { snakeCaseKey: { snakeCaseKey: [{ snakeCaseKey: 1 }] } },
    };
    const expected = {
      snake_case_key: {
        snake_case_key: { snake_case_key: [{ snake_case_key: 1 }] },
      },
    };
    expect(lodash.isEqual(camelCaseToSnakeCase(data), expected)).toBeTruthy();
  });
});
