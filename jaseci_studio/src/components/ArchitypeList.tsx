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
  Overlay,
  Button,
  SegmentedControl,
  LoadingOverlay,
  Tooltip,
} from "@mantine/core";
import { IconApi, IconCode, IconTrash } from "@tabler/icons";
import {
  UseMutateFunction,
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";
import dayjs from "dayjs";
import { SetStateAction } from "jotai";
import { Dispatch, useState } from "react";
import { Architype } from "../hooks/useRegisterArchetype";
import { client } from "./ReactQuery";

function ArchitypeList({
  setEditorValue,
  architypes,
  loading,
  setFilter,
  onRunWalker,
}: {
  onRunWalker: (walkerName: string) => void;
  setEditorValue: (value: string) => void;
  setFilter: Dispatch<SetStateAction<string>>;
  architypes: Architype[];
  loading: boolean;
}) {
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

        <Box sx={{ overflow: "scroll", height: "500px", position: "relative" }}>
          <LoadingOverlay visible={loading}></LoadingOverlay>
          <Stack p="xs" data-testid="architype-cards">
            {architypes?.map((architype) => (
              <ArchitypeCard
                onRunWalker={() => {
                  onRunWalker(architype.name);
                }}
                setEditorValue={setEditorValue}
                key={architype.jid}
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

export function ArchitypeCard({
  architype,
  removeArchitype,
  setEditorValue,
  onRunWalker,
}: {
  architype: Architype;
  removeArchitype: UseMutateFunction<any, any, string, unknown>;
  onRunWalker: () => void;
  setEditorValue: (value: string) => void;
}) {
  const [showDelete, setShowDelete] = useState(false);

  const loadArchitypeSrcCode = () => {
    const src = JSON.parse(architype.code_ir)?.ir?.src;
    setEditorValue(src);
  };

  return (
    <Card withBorder sx={{ position: "relative" }} onClick={() => {}}>
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

        <Group>
          {architype.kind === "walker" && (
            <Tooltip label="Run Walker">
              <ActionIcon
                color="blue"
                variant="light"
                size="xs"
                onClick={onRunWalker}
              >
                <IconApi></IconApi>
              </ActionIcon>
            </Tooltip>
          )}

          <Tooltip label="View Code">
            <ActionIcon
              color="teal"
              variant="light"
              size="xs"
              onClick={() => loadArchitypeSrcCode()}
            >
              <IconCode></IconCode>
            </ActionIcon>
          </Tooltip>

          <Tooltip label="Delete Architype">
            <ActionIcon
              color="red"
              variant="light"
              size="xs"
              onClick={() => setShowDelete(true)}
            >
              <IconTrash></IconTrash>
            </ActionIcon>
          </Tooltip>
        </Group>
      </Group>
    </Card>
  );
}

export default ArchitypeList;
