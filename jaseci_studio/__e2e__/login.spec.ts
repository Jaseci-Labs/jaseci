import { context } from "msw";
import { o } from "msw/lib/SetupApi-0d3126ba";
import { test, expect } from "../mocks/test";

test("login page loads", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Login/);
  const login = page.getByRole("heading", { name: "Login" });
  expect(await login.textContent()).toBe("Login");
});

test("testConnection works", async ({ page }) => {
  await page.goto("/");
  const host = page.getByRole("textbox", { name: "host" });
  const email = page.getByRole("textbox", { name: "email" });
  const password = page.getByRole("textbox", { name: "password" });

  await host.fill("http://mysite.com");
  await email.fill("admin@mail.com");
  await password.fill("password");

  const testConnectionBtn = page.getByText("Test Connection");
  await testConnectionBtn.click();

  const result = page.getByRole("alert", { name: "Result" });

  expect(await result.textContent()).toBe("Connection successful");
});

test("login works", async ({ page }) => {
  await page.goto("/");
  const host = page.getByRole("textbox", { name: "host" });
  const email = page.getByRole("textbox", { name: "email" });
  const password = page.getByRole("textbox", { name: "password" });

  await host.fill("http://mysite.com");
  await email.fill("admin@mail.com");
  await password.fill("password");

  const connectBtn = page.getByRole("button", { name: "Connect to Server" });

  const [_, __, result] = await Promise.all([
    page.waitForRequest("http://mysite.com/user/token/"),
    connectBtn.click(),
    page.waitForResponse("http://mysite.com/user/token/"),
  ]);

  expect(result.status()).toBe(200);
});
