import { zodResolver } from "@hookform/resolvers/zod";
import {
  Box,
  Card,
  Title,
  Stack,
  Grid,
  Text,
  Flex,
  Button,
  Alert,
  Transition,
} from "@mantine/core";
import { useForm } from "react-hook-form";
import { z } from "zod";
import FormTextField from "./FormTextField";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { setCookie } from "cookies-next";

const connectionSchema = z.object({
  email: z.string().email(),
  password: z.string(),
  host: z.string(),
  port: z.preprocess(Number, z.number()).optional(),
});

type LoginParams = Pick<
  z.infer<typeof connectionSchema>,
  "email" | "password"
> & { serverUrl: string };

export function LoginForm() {
  const [mode, setMode] = useState<"test" | "connect">();
  const router = useRouter();
  const { isLoading, error, data, mutateAsync } = useMutation({
    mutationFn: ({ serverUrl, email, password }: LoginParams) =>
      fetch(`${serverUrl}/user/token/`, {
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

  async function onSubmit(values: z.infer<typeof connectionSchema>) {
    const serverUrlHasScheme =
      values.host.startsWith("https://") || values.host.startsWith("http://");
    const serverUrl = `${serverUrlHasScheme ? "" : "http://"}${values.host}${
      values.port ? `:${values.port}` : ""
    }`;

    await mutateAsync(
      { serverUrl, email: values.email, password: values.password },
      {
        onSuccess: (data) => {
          if (mode === "connect") {
            if (data.token) {
              localStorage.setItem("token", data.token);
              localStorage.setItem("serverUrl", serverUrl);

              router.push("/dashboard");
            }
          }
        },
      }
    );
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

            <Transition
              mounted={data?.token || data?.non_field_errors || error}
              transition="fade"
              duration={400}
              timingFunction="ease"
            >
              {(styles) => (
                <div style={styles}>
                  {data?.token && (
                    <Alert color="green">Connection successful</Alert>
                  )}
                  {data?.non_field_errors && (
                    <Alert color="red">{data?.non_field_errors[0]}</Alert>
                  )}
                  {error && (
                    <Alert color="red">Unable to established connection</Alert>
                  )}
                </div>
              )}
            </Transition>
          </Stack>
        </form>
      </Card>
    </Box>
  );
}
