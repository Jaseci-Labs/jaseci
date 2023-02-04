import { MantineProvider } from "@mantine/core";
import { QueryClientProvider } from "@tanstack/react-query";
import { render, renderHook, screen, waitFor } from "@testing-library/react";
import { afterAll, beforeAll, expect, test } from "vitest";
import ArchitypeList from "../src/components/ArchitypeList";
import { setupServer } from "msw/node";
import handlers from "../mocks/handlers";
import architypeList from "../mocks/data/architype_list.json";
import { testQueryClient } from "../mocks/testQueryClient";
import useArchitypeList from "../src/hooks/useArtchitypeList";
import { renderWithClient } from "../mocks/utils";

const server = setupServer(...handlers);

beforeAll(() => {});

test("ArchitypeList", async () => {
  const result = renderWithClient(
    <MantineProvider>
      <ArchitypeList setEditorValue={() => {}} />
    </MantineProvider>
  );

  const cards = await result.findByTestId("architype-cards");

  expect(cards.childNodes.length).toBe(6);
});
