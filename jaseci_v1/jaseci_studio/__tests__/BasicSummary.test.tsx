import { MantineProvider } from "@mantine/core";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { test, expect } from "vitest";
import BasicSummary from "../src/components/BasicSummary";

test("BasicSummary", async () => {
  const queryClient = new QueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        <BasicSummary />
      </MantineProvider>
    </QueryClientProvider>
  );

  const heading = await screen.findByRole("heading", { name: "Summary" });
  const totalNodes = await screen.findByRole("heading", {
    name: "Total Nodes",
  });
  const totalWalkers = await screen.findByRole("heading", {
    name: "Total Walkers",
  });
  const totalEdges = await screen.findByRole("heading", {
    name: "Total Edges",
  });
  const totalGraphs = await screen.findByRole("heading", {
    name: "Total Graphs",
  });

  expect(heading.innerHTML).toContain("Summary");
  expect(totalNodes.innerHTML).toContain("0");
  expect(totalWalkers.innerHTML).toContain("0");
  expect(totalEdges.innerHTML).toContain("0");
  expect(totalGraphs.innerHTML).toContain("0");
});
