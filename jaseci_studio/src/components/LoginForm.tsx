"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import {
  Box,
  Card,
  Title,
  Stack,
  Grid,
  TextInput,
  Text,
  Flex,
  Button,
  Alert,
} from "@mantine/core";
import { useForm } from "react-hook-form";
import { z } from "zod";
import FormTextField from "./FormTextField";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";

const connectionSchema = z.object({
  email: z.string().email(),
  password: z.string(),
  host: z.string(),
  port: z.preprocess(Number, z.number()),
});

type LoginParams = z.infer<typeof connectionSchema>;

export function LoginForm() {
  const [mode, setMode] = useState<"test" | "connect">();
  const router = useRouter();
  const { isLoading, error, data, mutateAsync } = useMutation({
    mutationFn: ({ host, email, password, port }: LoginParams) =>
      fetch(`http://${host}:${port}/user/token/`, {
        method: "POST",
        body: JSON.stringify({
          email,
          password,
        }),
        headers: { "Content-Type": "application/json" },
      }).then((res) => res.json()),
  });

  const { control, handleSubmit } = useForm({
    resolver: zodResolver(connectionSchema),
  });

  async function onSubmit(values) {
    await mutateAsync(values, {
      onSuccess: (data) => {
        if (mode === "connect") {
          if (data.token) {
            localStorage.setItem("token", data.token);
            localStorage.setItem(
              "serverUrl",
              `http://${values.host}:${values.port}`
            );
            router.push("/dashboard");
          }
        }
      },
    });
  }

  return (
    <Box sx={{ display: "flex", alignItems: "center", height: "100vh" }}>
      <Card
        withBorder
        shadow={"md"}
        p={30}
        radius={"md"}
        sx={{ width: "95%", maxWidth: "600px", margin: "0 auto" }}
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <Box mb="xl">
            <Title>Login</Title>
            <Text color="gray">Connect to a server to start</Text>
          </Box>
          <Stack>
            <Grid sx={{ width: "100%", display: "flex" }} columns={6}>
              <Grid.Col span={4}>
                <FormTextField
                  required
                  control={control}
                  label="Host"
                  name="host"
                  placeholder="Enter host e.g localhost"
                ></FormTextField>
              </Grid.Col>
              <Grid.Col span={2}>
                <FormTextField
                  required
                  placeholder="Enter port e.g 8888"
                  name="port"
                  control={control}
                  label="Port"
                ></FormTextField>
              </Grid.Col>
            </Grid>
            <FormTextField
              required
              control={control}
              name="email"
              placeholder="Enter your email"
              label="Email"
            ></FormTextField>
            <FormTextField
              control={control}
              required
              placeholder="Enter your password"
              name="password"
              type="password"
              label="Password"
            ></FormTextField>
            <Flex justify="space-between" mt="lg">
              <Button
                loading={isLoading}
                type="submit"
                onClick={() => setMode("test")}
                color="gray"
              >
                Test Connection
              </Button>
              <Button
                loading={isLoading}
                type="submit"
                onClick={() => setMode("connect")}
                color="teal"
              >
                Connect
              </Button>
            </Flex>

            {data?.token && <Alert color="green">Connection successful</Alert>}
            {data?.non_field_errors && (
              <Alert color="red">{data?.non_field_errors[0]}</Alert>
            )}
            {error && (
              <Alert color="red">Unable to established connection</Alert>
            )}
          </Stack>
        </form>
      </Card>
    </Box>
  );
}
