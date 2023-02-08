import { QueryClient } from "@tanstack/react-query";

export const testQueryClient = new QueryClient({
  logger: {
    log: console.log,
    warn: console.warn,
    // ✅ no more errors on the console for tests
    error: process.env.NODE_ENV === "test" ? () => {} : console.error,
  },
  defaultOptions: {
    mutations: {
      cacheTime: 100000,
      retry: false,
    },
    queries: {
      cacheTime: 1000000,
      retry: false,
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      retryOnMount: false,
      retryDelay: 100000,
      refetchOnReconnect: false,
      staleTime: 1000000,
    },
  },
});
