import { test, expect } from "@playwright/test";

test("login page loads", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Login/);
  const login = page.getByRole("heading", { name: "Login" });
  expect(await login.textContent()).toBe("Login");
});

test("login works", async ({ page }) => {
  await page.goto("/");
  const host = page.getByRole("textbox", { name: "host" });
  const port = page.getByRole("textbox", { name: "port" });
  const email = page.getByRole("textbox", { name: "email" });
  const password = page.getByRole("textbox", { name: "password" });

  await host.fill("localhost");
  await port.fill("8200");
  await email.fill("admin@mail.com");
  await password.fill("password");

  const testConnection = page.getByText("Test Connection");

  //   const [response] = await Promise.all([
  //     await page.waitForResponse("http://localhost:8200/oauth/token"),
  //     testConnection.click(),
  //   ]);
  await testConnection.click();

  //   if (response.status() === 401) {
  const result = page.getByRole("alert");

  expect(await result.textContent()).toBe("Unable to establish connection");
  //   }
});
