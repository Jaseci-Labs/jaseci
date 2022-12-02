import {
  Box,
  Button,
  Card,
  Divider,
  Stack,
  TextInput,
  Title,
} from "@mantine/core";
import LogsViewer from "../components/LogsViewer/LogsViewer";
import { IBM_Plex_Mono } from "@next/font/google";
import {
  useDebouncedState,
  useDebouncedValue,
  useInputState,
} from "@mantine/hooks";

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400"],
});

function LogsPage() {
  const [searchTerm, setSearchTerm] = useDebouncedState("", 800);

  return (
    <Card shadow={"md"}>
      <Title order={3} mb={"xl"}>
        Logs
      </Title>
      <Card withBorder px={0} pt={0}>
        <Box p="xs">
          <TextInput
            label="Filter"
            variant="default"
            spellCheck="false"
            placeholder="Enter search term e.g jaseci, jaseci|objects, anything"
            size="xs"
            defaultValue={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          ></TextInput>
          <Stack align={"end"} mt="xs">
            <Button.Group>
              <Button variant="default" size="xs">
                Error
              </Button>
              <Button variant="default" size="xs">
                Warning
              </Button>
              <Button variant="default" size="xs">
                Info
              </Button>
            </Button.Group>
          </Stack>
        </Box>
        <Divider></Divider>
        <LogsViewer font={ibmPlexMono} searchTerm={searchTerm}></LogsViewer>
      </Card>
    </Card>
  );
}

export default LogsPage;
