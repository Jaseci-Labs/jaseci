import { MantineProvider } from "@mantine/core";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, renderHook, screen } from "@testing-library/react";
import RunWalker from "../src/components/RunWalker";
import { test, expect } from "vitest";
import architypes from "../mocks/data/architype_list.json";
import { createTestQueryClient } from "../mocks/utils";
import useRunWalker from "../src/hooks/useRunWalker";

test("RunWalker", async () => {
  const queryClient = new QueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        <RunWalker
          walker="get_imprint"
          walkers={[
            ...architypes.filter((architype) => architype.kind === "walker"),
          ]}
          setWalker={() => {}}
        />
      </MantineProvider>
    </QueryClientProvider>
  );

  const select = await screen.findByTestId("walker-select");
  expect(select.getAttribute("value")).toBe("get_imprint");

  const result = await screen.findByTestId("result");

  expect(result.innerHTML).toContain("Result");
});

test("useRunWalker hook", async () => {
  const wrapper = ({ children }) => (
    <QueryClientProvider client={createTestQueryClient()}>
      {children}
    </QueryClientProvider>
  );

  const {
    result: {
      current: { mutateAsync },
    },
  } = renderHook(() => useRunWalker(), {
    wrapper,
  });

  const result = await mutateAsync({
    walker: "get_imprint",
    nd: "",
    payload: {},
  });

  expect(result?.success).toBe(true);
});
