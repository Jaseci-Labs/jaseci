import { MantineProvider } from "@mantine/core";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { vi, test, expect } from "vitest";
import { LoginForm } from "../src/components/LoginForm";

vi.mock("next/navigation");

test("LoginForm", async () => {
  const queryClient = new QueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        <LoginForm />
      </MantineProvider>
    </QueryClientProvider>
  );

  const login = screen.getByRole("heading", { name: "Login" });
  const testConnectionBtn = screen.getByRole("button", {
    name: "Test Connection",
  });
  const connectBtn = screen.getByRole("button", { name: "Connect to Server" });

  expect(login.innerHTML).toContain("Login");
  expect(testConnectionBtn.innerHTML).toContain("Test Connection");
  expect(connectBtn.innerHTML).toContain("Connect");
});
