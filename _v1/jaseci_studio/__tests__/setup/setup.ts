import { afterAll, afterEach, beforeAll, vi } from "vitest";
import { server } from "../../mocks/server";
import { testQueryClient } from "../../mocks/testQueryClient";

beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" });
  global.ResizeObserver = class ResizeObserver {
    observe() {
      // do nothing
    }
    unobserve() {
      // do nothing
    }
    disconnect() {
      // do nothing
    }
  };
});

afterAll(() => server.close());

afterEach(() => {
  server.resetHandlers();
  testQueryClient.getQueryCache().clear();
});

Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});
