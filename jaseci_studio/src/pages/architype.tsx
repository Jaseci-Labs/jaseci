import {
  Flex,
  Card,
  Title,
  Button,
  Group,
  Box,
  Grid,
  Divider,
} from "@mantine/core";
import Editor from "../components/Editor";
import useRegisterArchetype from "../hooks/useRegisterArchetype";
import { useStudioEditor } from "../hooks/useStudioEditor";
import { getActiveSentinel } from "../hooks/useGetActiveSentinel";
import ArchitypeList from "../components/ArchitypeList";

function ArchetypePage() {
  const editor = useStudioEditor();
  const { data: activeSentinel, isLoading } = getActiveSentinel();
  const { mutate: registerArchitype } = useRegisterArchetype(
    editor.highlightError,
    editor.hideErrors
  );
  const { editorValue } = editor;

  return (
    <div>
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
              <ArchitypeList></ArchitypeList>
            </Grid.Col>

            <Grid.Col span={7}>
              <Editor editor={editor}></Editor>
            </Grid.Col>
          </Grid>
        </Card>
      </Flex>
    </div>
  );
}

export default ArchetypePage;
