import { Flex, Card, Title, Button, Group, Grid, Tabs } from "@mantine/core";
import Editor from "../components/Editor";
import useRegisterArchetype from "../hooks/useRegisterArchetype";
import { useStudioEditor } from "../hooks/useStudioEditor";
import { getActiveSentinel } from "../hooks/useGetActiveSentinel";
import ArchitypeList from "../components/ArchitypeList";
import useArchitypeList from "../hooks/useArtchitypeList";
import { useState } from "react";
import { IconApi, IconBrackets } from "@tabler/icons";
import RunWalker from "../components/RunWalker";

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
                setEditorValue={(value) => {
                  setTabId("editor");
                  setEditorValue(value);
                }}
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

export default ArchetypePage;
