import {
  JsonInput,
  Checkbox,
  TextInput,
  Group,
  Select,
  Button,
  Box,
  ThemeIcon,
  Divider,
  Text,
} from "@mantine/core";
import { Prism } from "@mantine/prism";
import { IconShieldCheck, IconShieldX } from "@tabler/icons";
import { Dispatch, SetStateAction, useState } from "react";
import { Architype } from "../hooks/useRegisterArchetype";
import useRunWalker from "../hooks/useRunWalker";

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
          sx={{ minWidth: "300px" }}
          data-testid="walker-select"
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
        data-testid="result"
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

export default RunWalker;
