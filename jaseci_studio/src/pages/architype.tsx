import {
  Flex,
  Card,
  Title,
  Button,
  Group,
  Grid,
  Tabs,
  JsonInput,
  Box,
  Text,
  Divider,
  Autocomplete,
  Select,
  TextInput,
  Checkbox,
  Badge,
  ThemeIcon,
} from "@mantine/core";
import Editor from "../components/Editor";
import useRegisterArchetype, { Architype } from "../hooks/useRegisterArchetype";
import { useStudioEditor } from "../hooks/useStudioEditor";
import { getActiveSentinel } from "../hooks/useGetActiveSentinel";
import ArchitypeList from "../components/ArchitypeList";
import useArchitypeList from "../hooks/useArtchitypeList";
import { Dispatch, useState } from "react";
import {
  IconApi,
  IconBrackets,
  IconShieldCheck,
  IconShieldX,
} from "@tabler/icons";
import useRunWalker from "../hooks/useRunWalker";
import { Prism } from "@mantine/prism";
import { SetStateAction } from "jotai";

function ArchetypePage() {
  const editor = useStudioEditor();
  const { data: activeSentinel } = getActiveSentinel();
  const { mutate: registerArchitype } = useRegisterArchetype(
    editor.highlightError,
    editor.hideErrors
  );
  const { editorValue, setEditorValue } = editor;

  const [walker, setWalker] = useState<string>(null);
  const [tabId, setTabId] = useState<string>("editor");

  const [filter, setFilter] = useState<"all" | "node" | "walker" | "edge">(
    "all"
  );
  const { data: architypes, isLoading: architypesLoading } = useArchitypeList({
    filter,
  });
  const { data: walkers, isLoading: walkersLoading } = useArchitypeList({
    filter: "walker",
  });

  // const openViewer = () => {
  //   if (typeof window !== "undefined") {
  //     invoke("open_graph_viewer");
  //   }
  // };

  return (
    <div>
      {/* <button onClick={() => openViewer()}>Open Graph Viewer</button> */}
      <Flex justify={"center"} align="center">
        <Card
          w="90%"
          h="90vh"
          withBorder
          shadow={"md"}
          radius="md"
          sx={{ margin: "0 auto", overflowY: "scroll" }}
          p={30}
        >
          <Group position="apart" align="start">
            <Title order={3} mb={"xl"}>
              Architypes
            </Title>
            <Button
              onClick={() =>
                registerArchitype({
                  code: editorValue,
                  snt: activeSentinel.jid,
                })
              }
              disabled={!activeSentinel?.jid}
            >
              Register Architype
            </Button>
          </Group>

          <Grid sx={{ height: "600px" }}>
            <Grid.Col span={5}>
              <ArchitypeList
                architypes={architypes}
                loading={architypesLoading}
                setFilter={setFilter}
                onRunWalker={(walkerName) => {
                  setWalker(walkerName);
                  setTabId("run_walker");
                }}
                setEditorValue={setEditorValue}
              ></ArchitypeList>
            </Grid.Col>

            <Grid.Col span={7}>
              <Tabs value={tabId} onTabChange={(tabId) => setTabId(tabId)}>
                <Tabs.List>
                  <Tabs.Tab value="editor" icon={<IconBrackets size={14} />}>
                    Editor
                  </Tabs.Tab>
                  <Tabs.Tab value="run_walker" icon={<IconApi size={14} />}>
                    Run Walker
                  </Tabs.Tab>
                </Tabs.List>
                <Tabs.Panel value="editor" pt="xs">
                  <Editor editor={editor}></Editor>
                </Tabs.Panel>
                <Tabs.Panel value="run_walker" pt="xs" sx={{ height: "100%" }}>
                  <RunWalker
                    walker={walker}
                    setWalker={setWalker}
                    walkers={walkers}
                  ></RunWalker>
                </Tabs.Panel>
              </Tabs>
            </Grid.Col>
          </Grid>
        </Card>
      </Flex>
    </div>
  );
}

function RunWalker({
  walkers,
  walker,
  setWalker,
}: {
  walker: string;
  setWalker: Dispatch<SetStateAction<string>>;
  walkers: Architype[];
}) {
  const [payload, setPayload] = useState<any>("{}");
  const [showNodeInput, setShowNodeInput] = useState<boolean>(false);
  const [node, setNode] = useState<string>(null);
  const { mutate: runWalker, data: result, isLoading } = useRunWalker();

  function runWalkerNow() {
    runWalker({
      payload: JSON.parse(payload || "{}"),
      walker,
      nd: node,
    });
  }

  return (
    <div>
      <JsonInput
        label="Enter Payload"
        placeholder="Enter payload to run walker"
        validationError="Invalid json"
        formatOnBlur
        autosize
        minRows={4}
        autoCorrect="off"
        autoCapitalize="off"
        autoComplete="off"
        value={payload}
        onChange={(value) => {
          setPayload(value);
        }}
      />

      {/* Checkbox to specify node */}
      <Checkbox
        label="Run on node"
        my="sm"
        onChange={(e) => {
          setShowNodeInput(e.currentTarget.checked);
        }}
      ></Checkbox>

      {showNodeInput && (
        <TextInput
          label="Node ID"
          placeholder="Enter node to run walker"
          value={node}
          onChange={(e) => setNode(e.currentTarget.value)}
        ></TextInput>
      )}

      <Group position="apart" my="sm">
        <Select
          label="Walker"
          placeholder="Pick a walker to run"
          searchable
          value={walker}
          onChange={(value) => setWalker(value)}
          data={(walkers || [])?.map((walker) => walker.name)}
        />
        <Button
          loading={isLoading}
          onClick={runWalkerNow}
          mt="md"
          color="teal"
          size="xs"
          disabled={!walker}
        >
          Run Now
        </Button>
      </Group>

      <Box
        sx={(theme) => ({
          background: theme.colors.gray[2],
          border: "1px solid " + theme.colors.gray[5],
          borderRadius: 8,
          minHeight: "300px",
          maxHeight: "400px",
          overflowY: "scroll",
        })}
        px="md"
        py="xs"
        my="lg"
      >
        <Group spacing={"xs"} mb="sm">
          <Text weight="bold">Result </Text>
          {result?.success ? (
            <ThemeIcon color="green" size="sm" radius="xl">
              <IconShieldCheck size={14}></IconShieldCheck>
            </ThemeIcon>
          ) : (
            <ThemeIcon color="red" size="sm" radius="xl">
              <IconShieldX size={14}></IconShieldX>
            </ThemeIcon>
          )}
        </Group>

        <Divider></Divider>

        <Prism language="json">
          {result
            ? JSON.stringify(result, null, 2)
            : "Run a walker to see the result"}
        </Prism>
      </Box>
    </div>
  );
}

export default ArchetypePage;
