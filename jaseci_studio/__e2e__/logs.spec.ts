import { test, expect } from "../mocks/test";

test("logs page loads", async ({ page }) => {
  await page.goto("/logs");
  await expect(page).toHaveTitle(/Logs/);
});
