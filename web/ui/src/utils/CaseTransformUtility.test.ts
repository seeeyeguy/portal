import lodash from "lodash";

import {
  camelCaseToSnakeCase,
  snakeCaseToCamelCase,
} from "utils/CaseTransformUtility";

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
