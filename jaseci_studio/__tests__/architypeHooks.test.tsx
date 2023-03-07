import useArchitypeList from "../src/hooks/useArtchitypeList";
import { QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { expect, test } from "vitest";
import { createTestQueryClient } from "../mocks/utils";
import architypeList from "../mocks/data/architype_list.json";
import useRegisterArchetype from "../src/hooks/useRegisterArchetype";
import architypeRegister from "../mocks/data/architype_register.json";

test("useArchitypeList hook", async () => {
  const wrapper = ({ children }) => (
    <QueryClientProvider client={createTestQueryClient()}>
      {children}
    </QueryClientProvider>
  );

  const { result } = renderHook(() => useArchitypeList({ filter: "all" }), {
    wrapper,
  });

  await waitFor(() => {
    expect(result.current.isSuccess).toBe(true);
  });

  expect(result.current.data?.length).toBe(architypeList.length);
});

test("registerArchitype hook", async () => {
  const wrapper = ({ children }) => (
    <QueryClientProvider client={createTestQueryClient()}>
      {children}
    </QueryClientProvider>
  );

  const { result } = renderHook(
    () =>
      useRegisterArchetype(
        () => {},
        () => {}
      ),
    {
      wrapper,
    }
  );

  await waitFor(() => {
    expect(result.current.mutateAsync).toBeTypeOf("function");
  });

  const newArchitype = await result.current.mutateAsync({
    code: "walker init {}",
    snt: "test",
  });

  expect(newArchitype).toStrictEqual(architypeRegister);
});
