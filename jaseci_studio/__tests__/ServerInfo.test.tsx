import { MantineProvider } from "@mantine/core";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { test, expect } from "vitest";
import ServerInfo from "../src/components/ServerInfo";

test("BasicSummary", async () => {
  const queryClient = new QueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        <ServerInfo />
      </MantineProvider>
    </QueryClientProvider>
  );

  const heading = await screen.findByRole("heading", { name: "Server Info" });

  const version = await screen.findByLabelText("version");
  const creator = await screen.findByLabelText("creator");
  const url = await screen.findByLabelText("url");
  const documentationUrl = await screen.findByLabelText("documentation url");

  expect(heading.innerHTML).toContain("Server Info");
  expect(version.innerHTML).toContain("0.0.0");
  expect(creator.innerHTML).toContain("Unknown");
  expect(url.innerHTML).toContain("Unknown");
  expect(documentationUrl.innerHTML).toContain("https://docs.jaseci.org");
});
