import {
  Alert,
  Box,
  Button,
  Card,
  Dialog,
  Flex,
  Group,
  LoadingOverlay,
  Modal,
  Pagination,
  Table,
  TextInput,
  Title,
} from "@mantine/core";
import { useDebouncedValue } from "@mantine/hooks";
import { showNotification } from "@mantine/notifications";
import { IconVectorTriangle } from "@tabler/icons";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { ChangeGraphModal } from "../../components/ChangeGraphModal";
import { client } from "../../components/ReactQuery";
import useUserInfo from "../../hooks/useUserInfo";

function GraphViewerPage() {
  const [opened, setOpened] = useState(false);
  const [activeGraph, setActiveGraph] = useState("");
  const [activeGraphUser, setActiveGraphUser] = useState("");
  const { data: user } = useUserInfo();

  return (
    <>
      <Flex justify={"center"}>
        <Card
          w="100%"
          h="100%"
          withBorder
          shadow={"md"}
          p={8}
          radius={"md"}
          sx={{ margin: "0 auto" }}
        >
          <Group position="apart">
            <Title order={3} mb={"xl"}>
              Graph
            </Title>

            {activeGraphUser && (
              <Alert variant="light">Viewing Graph of {activeGraphUser}</Alert>
            )}

            {user?.is_superuser ? (
              <>
                <Button
                  leftIcon={<IconVectorTriangle></IconVectorTriangle>}
                  onClick={() => setOpened(true)}
                >
                  Change Graph
                </Button>

                <ChangeGraphModal
                  opened={opened}
                  onClose={() => {
                    setOpened(false);
                  }}
                  onChangeActiveGraph={(jid, user) => {
                    setActiveGraph(jid);
                    setActiveGraphUser(user);
                  }}
                ></ChangeGraphModal>
              </>
            ) : (
              <></>
            )}
          </Group>

          <jsc-graph
            height="85vh"
            serverUrl="http://localhost:8888"
            graphId={activeGraph}
          ></jsc-graph>
        </Card>
      </Flex>
    </>
  );
}

export default GraphViewerPage;

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "jsc-graph": { height: string; serverUrl: string; graphId?: string };
    }
  }
}
