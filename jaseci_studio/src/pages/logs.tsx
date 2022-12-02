import {
  ActionIcon,
  Box,
  Card,
  Divider,
  Flex,
  Group,
  Select,
  TextInput,
  Title,
  Tooltip,
} from "@mantine/core";
import LogsViewer from "../components/LogsViewer/LogsViewer";
import { IBM_Plex_Mono } from "@next/font/google";
import { useDebouncedState } from "@mantine/hooks";
import LevelFilter from "../components/LogsViewer/LevelFilter";
import { IconArrowDown, IconArrowUp, IconPlayerPause } from "@tabler/icons";
import Head from "next/head";

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400"],
});

function LogsPage() {
  const [searchTerm, setSearchTerm] = useDebouncedState("", 800);

  return (
    <>
      <Head>
        <title>Logs</title>
      </Head>

      <Flex justify={"center"} align="center">
        <Card
          w="90%"
          h="90%"
          withBorder
          shadow={"md"}
          radius="md"
          sx={{ margin: "0 auto" }}
          p={30}
        >
          <Title order={3} mb={"xl"}>
            Logs
          </Title>
          <Card withBorder px={0} pt={0} sx={{ maxHeight: "90vh" }}>
            <Box p="xs">
              <TextInput
                label="Filter"
                variant="default"
                spellCheck="false"
                placeholder="Enter search term e.g jaseci, jaseci|objects, anything"
                size="xs"
                defaultValue={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              ></TextInput>
              <Flex justify="space-between" mt="xs">
                <Group>
                  <Select
                    aria-label="Choose Time"
                    placeholder="Choose Time"
                    size="xs"
                    variant="default"
                    defaultValue="realTime"
                    data={[
                      { value: "realTime", label: "Real-time" },
                      { value: "lastHour", label: "Last Hour" },
                      { value: "last3Hours", label: "Last 3 Hours" },
                      { value: "Last Day", label: "Last Day" },
                    ]}
                  />

                  <Tooltip label="Pause Logs" withArrow>
                    <ActionIcon variant="light" color="orange">
                      <IconPlayerPause size={16} />
                    </ActionIcon>
                  </Tooltip>

                  <Tooltip label="Scroll to Top" withArrow>
                    <ActionIcon variant="light" color="orange">
                      <IconArrowUp size={16} />
                    </ActionIcon>
                  </Tooltip>

                  <Tooltip label="Scroll to Bottom" withArrow>
                    <ActionIcon variant="light" color="orange">
                      <IconArrowDown size={16} />
                    </ActionIcon>
                  </Tooltip>
                </Group>

                <LevelFilter></LevelFilter>
              </Flex>
            </Box>
            <Divider></Divider>
            <LogsViewer font={ibmPlexMono} searchTerm={searchTerm}></LogsViewer>
          </Card>
        </Card>
      </Flex>
    </>
  );
}

export default LogsPage;
