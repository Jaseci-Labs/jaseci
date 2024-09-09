import { test, expect } from "../mocks/test";

test.skip("logs messages load", async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem("serverUrl", "http://localhost:8005");
    window.localStorage.setItem("token", "abcde");
  });

  await page.goto("/logs");
  await page.waitForRequest("http://localhost:8005/js_admin/logger_get");

  const messages = page.getByRole("table").locator("tr");
  const firstMessageCells = messages.first().getByRole("cell");
  const dateAndTimeCell = firstMessageCells.nth(0);
  const messageCell = firstMessageCells.nth(1);

  expect(await messages.count()).toBe(9);
  expect(await firstMessageCells.count()).toBe(2);
  expect(await dateAndTimeCell.innerHTML()).toContain("2022-12-02");
  expect(await dateAndTimeCell.innerHTML()).toContain("03:30:11.027");
  expect(await messageCell.innerText()).toBe(
    "INFO - post_run: JsOrc is not automated."
  );
});

test("pause logs works", async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem("serverUrl", "http://localhost:8005");
    window.localStorage.setItem("token", "abcde");
  });

  await page.goto("/logs");

  const pauseLogs = page.getByRole("button", { name: /pause logs/i });
  const pauseLogsTooltip = page.getByTestId("pause-logs");

  await pauseLogs.hover();
  expect(await pauseLogsTooltip.innerText()).toBe("Pause Logs");

  await pauseLogs.click();

  await pauseLogs.hover();
  expect(await pauseLogsTooltip.innerText()).toBe("Resume Logs");
});

test("scroll buttons", async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem("serverUrl", "http://localhost:8005");
    window.localStorage.setItem("token", "abcde");
  });

  await page.goto("/logs");

  const scrollToTopBtn = page.getByRole("button", { name: /scroll to top/i });
  const scrollToTopTooltip = page.getByTestId("scroll-to-top");

  await scrollToTopBtn.hover();
  expect(await scrollToTopTooltip.innerText()).toBe("Scroll to Top");

  const scrollToBottomBtn = page.getByRole("button", {
    name: /scroll to bottom/i,
  });
  const scrollToBottomTooltip = page.getByTestId("scroll-to-bottom");

  await scrollToBottomBtn.hover();
  expect(await scrollToBottomTooltip.innerText()).toBe("Scroll to Bottom");
});
