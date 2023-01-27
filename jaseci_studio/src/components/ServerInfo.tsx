import { Card, Title, Text, Stack, Divider, Anchor } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { client } from "./ReactQuery";

function ServerInfo() {
  const { data } = useQuery({
    queryKey: ["serverInfo"],
    queryFn: () => {
      return client.post("/js_public/info").then((res) => res.data);
    },
    placeholderData: {
      Version: "0.0.0",
      Creator: "Unknown",
      URL: "Unknown",
    },
  });

  return (
    <Card
      withBorder
      shadow={"md"}
      p={30}
      radius={"md"}
      sx={{ margin: "0 auto" }}
    >
      <Title order={3} mb="lg">
        Server Info
      </Title>
      <Stack spacing={2}>
        <div aria-label="version">
          <Divider label="Version" />
          <Text component="span" weight={"normal"} color="dimmed">
            {data?.Version}
          </Text>
        </div>

        <div aria-label="creator">
          <Divider label="Creator" />
          <Text component="span" weight={"normal"} color="dimmed">
            {data?.Creator}
          </Text>
        </div>

        <div aria-label="url">
          <Divider label="URL" />
          <Anchor component="span" color="dimmed">
            {data?.URL}
          </Anchor>
        </div>

        <div aria-label="documentation url">
          <Divider label="Documentation" />
          <Anchor component="span" color="dimmed">
            https://docs.jaseci.org
          </Anchor>
        </div>
      </Stack>
    </Card>
  );
}

export default ServerInfo;
