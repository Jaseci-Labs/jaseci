import { MantineProvider } from "@mantine/core";
import { renderHook } from "@testing-library/react";
import { expect, test } from "vitest";
import ArchitypeList, { ArchitypeCard } from "../src/components/ArchitypeList";
import { renderWithClient } from "../mocks/utils";
import { useState } from "react";
import architypeList from "../mocks/data/architype_list.json";

test("ArchitypeList", async () => {
  // use state hook
  const { result: state } = renderHook(() => useState("all"));
  const [_filter, setFilter] = state.current;

  const result = renderWithClient(
    <MantineProvider>
      <ArchitypeList
        setEditorValue={() => {}}
        setFilter={setFilter}
        architypes={architypeList}
        loading={false}
      />
    </MantineProvider>
  );

  const cards = result.getByTestId("architype-cards");
  expect(cards.childNodes.length).toBe(50);
});

test("ArchitypeCard component", async () => {
  const architype = architypeList[0];
  const result = renderWithClient(
    <MantineProvider>
      <ArchitypeCard
        architype={architype}
        setEditorValue={() => {}}
        removeArchitype={() => {}}
      />
    </MantineProvider>
  );

  expect(result.container.innerHTML).toContain(architype.name);
  expect(result.container.innerHTML).toContain(architype.kind);
});
