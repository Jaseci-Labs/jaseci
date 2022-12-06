import { test, expect } from "../mocks/test";

test("logs page loads", async ({ page }) => {
  await page.goto("/logs");
  await expect(page).toHaveTitle(/Logs/);
});

test("logs messages load", async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem("serverUrl", "http://mysite.com");
    window.localStorage.setItem("token", "abcde");
  });

  await page.goto("/logs");
  await page.waitForRequest("http://mysite.com/js_admin/logger_get");

  const messages = page.getByRole("table").locator("tr");
  const firstMessageCells = messages.first().getByRole("cell");
  const dateAndTimeCell = firstMessageCells.nth(0);
  const messageCell = firstMessageCells.nth(1);

  expect(await messages.count()).toBe(8);
  expect(await firstMessageCells.count()).toBe(2);
  expect(await dateAndTimeCell.innerHTML()).toContain("2022-12-02");
  expect(await dateAndTimeCell.innerHTML()).toContain("03:30:11.027");
  expect(await messageCell.innerText()).toBe(
    "INFO - post_run: JsOrc is not automated."
  );
});
