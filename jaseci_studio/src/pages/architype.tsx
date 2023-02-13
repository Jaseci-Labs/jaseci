import { Flex, Card, Title, Button, Group, Grid } from "@mantine/core";
import Editor from "../components/Editor";
import useRegisterArchetype from "../hooks/useRegisterArchetype";
import { useStudioEditor } from "../hooks/useStudioEditor";
import { getActiveSentinel } from "../hooks/useGetActiveSentinel";
import ArchitypeList from "../components/ArchitypeList";
import useArchitypeList from "../hooks/useArtchitypeList";
import { useState } from "react";
import useGuard from "../hooks/useGuard";

function ArchetypePage() {
  const { granted } = useGuard({ roles: ["superuser"] });
  const editor = useStudioEditor();
  const { data: activeSentinel } = getActiveSentinel();
  const { mutate: registerArchitype } = useRegisterArchetype(
    editor.highlightError,
    editor.hideErrors
  );
  const { editorValue, setEditorValue } = editor;

  const [filter, setFilter] = useState<"all" | "node" | "walker" | "edge">(
    "all"
  );
  const { data: architypes, isLoading: architypesLoading } = useArchitypeList({
    filter,
  });

  // const openViewer = () => {
  //   if (typeof window !== "undefined") {
  //     invoke("open_graph_viewer");
  //   }
  // };

  return (
    <div>
      {granted ? (
        <Flex justify={"center"} align="center">
          <Card
            w="90%"
            h="90vh"
            withBorder
            shadow={"md"}
            radius="md"
            sx={{ margin: "0 auto" }}
            p={30}
          >
            {JSON.stringify(granted)}
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
                  setEditorValue={setEditorValue}
                ></ArchitypeList>
              </Grid.Col>

              <Grid.Col span={7}>
                <Editor editor={editor}></Editor>
              </Grid.Col>
            </Grid>
          </Card>
        </Flex>
      ) : (
        <></>
      )}
    </div>
  );
}

export default ArchetypePage;
