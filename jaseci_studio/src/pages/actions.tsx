import {
  Button,
  Card,
  Divider,
  Flex,
  Grid,
  List,
  Modal,
  ThemeIcon,
  Title,
} from "@mantine/core";
import LogsViewer from "../components/LogsViewer/LogsViewer";
import { IBM_Plex_Mono } from "@next/font/google";
import { useDebouncedState, useScrollIntoView } from "@mantine/hooks";
import LevelFilter from "../components/LogsViewer/LevelFilter";
import {
  IconArrowDown,
  IconArrowUp,
  IconCircleCheck,
  IconCircleDashed,
  IconPlayerPause,
  IconPlayerPlay,
} from "@tabler/icons";
import Head from "next/head";
import { useEffect, useState } from "react";

function ManageActionsPage() {
  const [opened, setOpened] = useState(false);
  const actions = [
    { name: "action_item_1" },
    { name: "action_item_2" },
    { name: "action_item_3" },
    { name: "action_item_4" },
    { name: "action_item_5" },
    { name: "action_item_6" },
    { name: "action_item_7" },
  ];

  return (
    <>
      <Head>
        <title>Logs</title>
      </Head>

      <Flex justify={"center"} align="center">
        <Card
          w="90%"
          h="600px"
          withBorder
          shadow={"md"}
          radius="md"
          sx={{ margin: "0 auto" }}
          p={30}
        >
          <Flex justify="space-between">
            <Title order={3} mb={"xl"}>
              Manage Actions
            </Title>
            <Button onClick={() => setOpened(true)}>Upload Action</Button>
          </Flex>

          <Grid>
            <Grid.Col span={5}>
              <Title order={4}>Available Actions</Title>
              <Divider></Divider>

              <List
                spacing="xs"
                size="sm"
                center
                icon={
                  <ThemeIcon color="teal" size={24} radius="xl">
                    <IconCircleDashed size={16} />
                  </ThemeIcon>
                }
                sx={{ paddingTop: "20px" }}
              >
                {actions.slice(0, 4).map((action) => (
                  <List.Item key={action.name}>
                    <span>{action.name}</span>
                    <Button
                      size="xs"
                      sx={{ marginLeft: "12px" }}
                      variant="light"
                    >
                      Load
                    </Button>
                  </List.Item>
                ))}
              </List>
            </Grid.Col>

            <Grid.Col span={7}>
              <Title order={4}>Loaded Actions</Title>
              <Divider></Divider>

              <List
                spacing="xs"
                size="sm"
                center
                icon={
                  <ThemeIcon color="teal" size={24} radius="xl">
                    <IconCircleCheck size={16} />
                  </ThemeIcon>
                }
                sx={{ paddingTop: "20px" }}
              >
                {actions.slice(4).map((action) => (
                  <List.Item key={action.name}>
                    {action.name}
                    <Button
                      size="xs"
                      sx={{ marginLeft: "12px" }}
                      variant="light"
                    >
                      Unload
                    </Button>
                  </List.Item>
                ))}
              </List>
            </Grid.Col>
          </Grid>
        </Card>

        <Modal
          opened={opened}
          onClose={() => setOpened(false)}
          title="Upload Action"
        >
          {/* Modal content */}
        </Modal>
      </Flex>
    </>
  );
}

export default ManageActionsPage;
