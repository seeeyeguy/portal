import { setupServer } from "msw/node";
import "@testing-library/jest-dom/vitest";

import handlers from "./src/tests/mocks/HandlerMocks";

const server = setupServer(...handlers);

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterAll(() => server.close());
afterEach(() => server.resetHandlers());
