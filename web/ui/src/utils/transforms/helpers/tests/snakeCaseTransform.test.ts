import lodash from "lodash";

import { snakeCaseToCamelCase } from "utils/transforms/helpers";

describe("Test `snakeCaseToCamelCase` transform function", () => {
  test("Transform array of objects", () => {
    const data = [{ snake_case_key: [{ snake_case_key: 1 }] }];
    const expected = [{ snakeCaseKey: [{ snakeCaseKey: 1 }] }];
    expect(lodash.isEqual(snakeCaseToCamelCase(data), expected)).toBeTruthy();
  });
  test("Transform object of objects", () => {
    const data = {
      snake_case_key: {
        snake_case_key: { snake_case_key: [{ snake_case_key: 1 }] },
      },
    };
    const expected = {
      snakeCaseKey: { snakeCaseKey: { snakeCaseKey: [{ snakeCaseKey: 1 }] } },
    };
    expect(lodash.isEqual(snakeCaseToCamelCase(data), expected)).toBeTruthy();
  });
});
