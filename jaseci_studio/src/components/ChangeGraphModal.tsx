import {
  Modal,
  Box,
  TextInput,
  Table,
  LoadingOverlay,
  Button,
  Pagination,
} from "@mantine/core";
import { useDebouncedValue } from "@mantine/hooks";
import { showNotification } from "@mantine/notifications";
import { useState, useEffect } from "react";
import { useGetDetailedObject } from "../hooks/useGetDetailedObject";
import { useGetMasterAllUsers } from "../hooks/useGetMasterAllUsers";

export function ChangeGraphModal({
  opened,
  onClose,
  onChangeActiveGraph,
}: {
  opened: boolean;
  onClose: () => void;
  onChangeActiveGraph: (activeGraph: string, user: string) => void;
}) {
  const LIMIT = 10;
  const [activePage, setActivePage] = useState(1);
  const [search, setSearch] = useState("");
  const [debouncedSearch] = useDebouncedValue(search, 200);
  const { data, isLoading, isSuccess } = useGetMasterAllUsers({
    limit: LIMIT,
    search: debouncedSearch,
    offset: activePage === 1 ? 0 : (activePage - 1) * LIMIT,
  });

  const { mutate: getDetailedUserObject } = useGetDetailedObject();
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
            <LoadingOverlay visible={isLoading}></LoadingOverlay>
            <Table withBorder>
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
