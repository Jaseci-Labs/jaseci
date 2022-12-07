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
import { useDebouncedState, useScrollIntoView } from "@mantine/hooks";
import LevelFilter from "../components/LogsViewer/LevelFilter";
import {
  IconArrowDown,
  IconArrowUp,
  IconPlayerPause,
  IconPlayerPlay,
} from "@tabler/icons";
import Head from "next/head";
import { useEffect, useState } from "react";

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400"],
});

function LogsPage() {
  const [searchTerm, setSearchTerm] = useDebouncedState("", 800);
  const [level, setLevel] = useState<"ERROR" | "INFO" | "WARNING" | null>(null);
  const [paused, setPaused] = useState(false);
  const {
    scrollIntoView: scrollToLog,
    targetRef: scrollTargetRef,
    scrollableRef,
  } = useScrollIntoView<HTMLTableRowElement>({
    offset: 0,
    onScrollFinish: () => setScrollDirection(null),
    easing: (t) =>
      t < 0.5 ? 16 * Math.pow(t, 5) : 1 - Math.pow(-2 * t + 2, 5) / 2,
  });
  const [scrollDirection, setScrollDirection] = useState<
    "top" | "bottom" | null
  >("bottom");

  useEffect(() => {
    scrollToLog({ alignment: "start" });
  }, [scrollDirection]);

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

                  <Tooltip
                    label={paused ? "Resume Logs" : "Pause Logs"}
                    withArrow
                  >
                    <ActionIcon
                      onClick={() => setPaused((prevValue) => !prevValue)}
                      variant="light"
                      color="orange"
                    >
                      {paused ? (
                        <IconPlayerPlay size={16}> </IconPlayerPlay>
                      ) : (
                        <IconPlayerPause size={16} />
                      )}
                    </ActionIcon>
                  </Tooltip>

                  <Tooltip label="Scroll to Top" withArrow>
                    <ActionIcon
                      variant="light"
                      color="orange"
                      onClick={() => {
                        setScrollDirection("top");
                      }}
                    >
                      <IconArrowUp size={16} />
                    </ActionIcon>
                  </Tooltip>

                  <Tooltip label="Scroll to Bottom" withArrow>
                    <ActionIcon
                      variant="light"
                      color="orange"
                      onClick={() => {
                        setScrollDirection("bottom");
                      }}
                    >
                      <IconArrowDown size={16} />
                    </ActionIcon>
                  </Tooltip>
                </Group>

                <LevelFilter setLevel={setLevel} level={level}></LevelFilter>
              </Flex>
            </Box>
            <Divider></Divider>
            <LogsViewer
              scrollDirection={scrollDirection}
              scrollRefs={[scrollTargetRef, scrollableRef]}
              paused={paused}
              level={level}
              font={ibmPlexMono}
              searchTerm={searchTerm}
            ></LogsViewer>
          </Card>
        </Card>
      </Flex>
    </>
  );
}

export default LogsPage;
