import {
  Box,
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
import {
  IconCircleCheck,
  IconCircleDashed,
  IconGitBranchDeleted,
} from "@tabler/icons";
import Head from "next/head";
import { useState } from "react";
import LoadedActions from "../components/LoadedActions";
import useGuard from "../hooks/useGuard";

function ManageActionsPage() {
  const { granted } = useGuard({ roles: ["superuser"] });
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
      {granted ? (
        <>
          <Head>
            <title>Logs</title>
          </Head>

          <Flex justify={"center"} align="center">
            <Card
              w="90%"
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
                <Button onClick={() => setOpened(true)}>Import Action</Button>
              </Flex>

              <Grid>
                <Grid.Col span={12}>
                  <Title order={4}>Available Modules</Title>
                  <Divider></Divider>
                  <Box sx={{ display: "flex", justifyContent: "center" }}>
                    <LoadedActions></LoadedActions>
                  </Box>
                </Grid.Col>
              </Grid>
            </Card>

            <Modal
              opened={opened}
              onClose={() => setOpened(false)}
              title="Import Action"
            >
              {/* Modal content */}
            </Modal>
          </Flex>
        </>
      ) : null}
    </>
  );
}

export default ManageActionsPage;
