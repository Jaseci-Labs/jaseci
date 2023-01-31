import {
  Box,
  Card,
  Text,
  Divider,
  Title,
  Stack,
  Flex,
  Badge,
  Group,
  ActionIcon,
  Popover,
  Overlay,
  Button,
  SegmentedControl,
  LoadingOverlay,
} from "@mantine/core";
import { IconTrash } from "@tabler/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import dayjs from "dayjs";
import { useState } from "react";
import { Architype } from "../hooks/useRegisterArchetype";
import { client } from "./ReactQuery";

function ArchitypeList() {
  const [filter, setFilter] = useState<"all" | "node" | "walker" | "edge">(
    "all"
  );

  const { data: architypes, isLoading: architypesLoading } = useQuery(
    ["architypes", filter],
    () =>
      client
        .post<Architype[]>("/js/architype_list", {
          kind: filter === "all" ? undefined : filter,
        })
        .then((res) => res.data)
  );

  const queryClient = useQueryClient();

  // remove architype
  const { mutate: removeArchitype } = useMutation(
    (jid: string) =>
      client
        .post("/js/architype_delete", {
          arch: jid,
        })
        .then((res) => res.data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["architypes"]);
      },
    }
  );

  return (
    <>
      <Box
        sx={{
          width: "100%",
          height: "100%",
          overflowY: "auto",
          background: "#f5f5f5",
        }}
        px={"md"}
        py="md"
      >
        <Title order={5} mb="md">
          All Architypes
        </Title>
        <Divider></Divider>
        <SegmentedControl
          data={[
            { label: "All", value: "all" },
            { label: "Nodes", value: "node" },
            { label: "Walkers", value: "walker" },
            { label: "Edges", value: "edge" },
          ]}
          onChange={(value) => setFilter(value as any)}
        />
        <Divider mb="md"></Divider>
        {/* {JSON.stringify(architypes)} */}
        <Box sx={{ overflow: "scroll", height: "500px", position: "relative" }}>
          <LoadingOverlay visible={architypesLoading}></LoadingOverlay>
          <Stack p="xs">
            {architypes?.map((architype) => (
              <ArchitypeCard
                architype={architype}
                removeArchitype={removeArchitype}
              ></ArchitypeCard>
            ))}
          </Stack>
        </Box>
      </Box>
    </>
  );
}

function ArchitypeCard({ architype, removeArchitype }) {
  const [showDelete, setShowDelete] = useState(false);
  return (
    <Card key={architype.jid} withBorder sx={{ position: "relative" }}>
      <Group position="apart" align="start">
        <Flex gap={"xs"} align="center" mb="xs">
          <Text size="sm">{architype.name}</Text>
          <Badge size="xs">{architype.kind}</Badge>
        </Flex>

        {showDelete && <Overlay opacity={0.8} color="#000" zIndex={5} />}
        {showDelete && (
          <Box
            sx={{
              position: "absolute",
              zIndex: 6,
              width: "75%",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
            }}
          >
            <Text sx={{ color: "#fff" }}>Delete this architype?</Text>
            <Group position="apart">
              <Button size="xs" onClick={() => removeArchitype(architype.jid)}>
                Yes
              </Button>
              <Button size="xs" onClick={() => setShowDelete(false)}>
                No
              </Button>
            </Group>
          </Box>
        )}
      </Group>

      <Group position="apart" align="center">
        <Text color="gray" size="xs">
          {dayjs(architype.j_timestamp).format("DD/MM/YYYY HH:mm:ss A")}
        </Text>

        <ActionIcon
          color="red"
          variant="light"
          size="xs"
          onClick={() => setShowDelete(true)}
        >
          <IconTrash></IconTrash>
        </ActionIcon>
      </Group>
    </Card>
  );
}

export default ArchitypeList;
