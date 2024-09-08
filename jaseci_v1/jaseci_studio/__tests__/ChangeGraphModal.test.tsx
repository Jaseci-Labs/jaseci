import { MantineProvider } from "@mantine/core";
import { expect, test } from "vitest";
import { renderWithClient } from "../mocks/utils";
import { ChangeGraphModal } from "../src/components/ChangeGraphModal";

test("it renders", async () => {
  const result = renderWithClient(
    <MantineProvider>
      <ChangeGraphModal
        opened={true}
        onClose={() => {}}
        onChangeActiveGraph={() => {}}
      ></ChangeGraphModal>
    </MantineProvider>
  );

  const table = await result.findByRole("table");

  expect(table).toBeTruthy();
  expect(table.innerHTML).toContain("Name");
  expect(table.innerHTML).toContain("Email");
  expect(table.innerHTML).toContain("Action");
  expect(table.querySelectorAll("tr").length).toBe(1);
});
