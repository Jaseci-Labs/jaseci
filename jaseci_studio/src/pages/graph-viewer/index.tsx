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
import { client } from "../../components/ReactQuery";

function GraphViewerPage() {
  const [opened, setOpened] = useState(false);
  const [activeGraph, setActiveGraph] = useState("");
  const [activeGraphUser, setActiveGraphUser] = useState("");

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

type User = {
  id: number;
  user: string;
  jid: string;
  name: string;
  created_date: string;
  is_activated: boolean;
  is_superuser: boolean;
};

type DetailedUserObject = {
  name: string;
  kind: string;
  jid: string;
  j_timestamp: string;
  j_type: string;
  j_parent: string;
  j_master: string;
  j_access: string;
  j_r_acc_ids: string[];
  j_rw_acc_ids: string[];
  caller: string;
  head_master_id: string;
  sub_master_ids: string[];
  alias_map: {};
  perm_default: string;
  active_gph_id: string;
  graph_ids: string[];
  spawned_walker_ids: string[];
  yielded_walkers_ids: string[];
  active_snt_id: string;
  sentinel_ids: string[];
};

const useMasterAllUsers = ({
  search,
  offset,
  limit,
}: {
  search: string;
  offset: number;
  limit: number;
}) => {
  let LIMIT = 1;

  return useQuery(["master_allusers", search, offset], async () => {
    const response = await client.post<{ data: User[]; total: number }>(
      "/js_admin/master_allusers",
      { search, offset, limit: LIMIT }
    );

    return response.data;
  });
};

const useGetDetailedUserObject = () => {
  return useMutation(async (jid: string) => {
    const response = await client.post<DetailedUserObject>("/js/object_get", {
      obj: jid,
      detailed: true,
    });

    return response.data;
  });
};

function ChangeGraphModal({
  opened,
  onClose,
  onChangeActiveGraph,
}: {
  opened: boolean;
  onClose: () => void;
  onChangeActiveGraph: (activeGraph: string, user: string) => void;
}) {
  const LIMIT = 1;
  const [activePage, setActivePage] = useState(1);
  const [search, setSearch] = useState("");
  const [debouncedSearch] = useDebouncedValue(search, 200);
  const { data, isLoading, isSuccess } = useMasterAllUsers({
    limit: LIMIT,
    search: debouncedSearch,
    offset: activePage === 1 ? 0 : (activePage - 1) * LIMIT,
  });
  const { mutate: getDetailedUserObject } = useGetDetailedUserObject();
  const [activeGraph, setActiveGraph] = useState("");
  const [activeGraphUser, setActiveGraphUser] = useState("");

  useEffect(() => {
    if (activeGraph && onChangeActiveGraph && activeGraphUser)
      onChangeActiveGraph(activeGraph, activeGraphUser);
  }, [activeGraph, activeGraphUser]);

  return (
    <>
      <Modal size="lg" title="Change Graph" opened={opened} onClose={onClose}>
        <Box w="100%" h="100%">
          <TextInput
            name="Search"
            mb="sm"
            spellCheck={false}
            label="Search Users"
            placeholder="Search all users"
            value={search}
            onChange={(e) => {
              setActivePage(1);
              setSearch(e.currentTarget.value);
            }}
          ></TextInput>

          <Box sx={{ position: "relative" }}>
            <Table withBorder>
              <LoadingOverlay visible={isLoading}></LoadingOverlay>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {isSuccess &&
                  data?.data?.map((user) => (
                    <tr>
                      <td>{user.name || "___"}</td>
                      <td>{user.user}</td>
                      <td>
                        <Button
                          size="xs"
                          onClick={() => {
                            getDetailedUserObject(user.jid, {
                              onSuccess: (data) => {
                                if (!data.active_gph_id) {
                                  showNotification({
                                    id: "no-active-graph-" + user.jid,
                                    title: "No active graph!",
                                    message: `User [${user.user}] does not have an active graph.`,
                                    color: "red",
                                  });

                                  return;
                                }

                                setActiveGraph(data.active_gph_id);
                                setActiveGraphUser(user.user);
                                showNotification({
                                  id: "graph-changed" + user.jid,
                                  title: "Graph Changed",
                                  message: "Now using graph of " + user.user,
                                  color: "teal",
                                });

                                onClose();
                              },
                            });
                          }}
                        >
                          Use Graph
                        </Button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </Table>
          </Box>

          <Pagination
            total={Math.ceil(data?.total / 1)}
            page={activePage}
            onChange={setActivePage}
            disabled={!data?.total}
            my="lg"
          ></Pagination>
        </Box>
      </Modal>
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
