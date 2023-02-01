import { Accordion, Box, Button, Stack, useMantineTheme } from "@mantine/core";
import { IconGitBranchDeleted } from "@tabler/icons";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { client } from "./ReactQuery";

function LoadedActions() {
  const { data } = useQuery({
    queryKey: ["loadedActions"],
    queryFn: () => {
      return client
        .post("/js_admin/actions_module_list", { detailed: true })
        .then((res) => res.data)
        .then((value) => ({
          loadedActions: value,
        }));
    },
  });

  const theme = useMantineTheme();
  const getColor = (color: string) =>
    theme.colors[color][theme.colorScheme === "dark" ? 5 : 7];

  return (
    <>
      <Accordion
        chevronPosition="left"
        variant="separated"
        radius="md"
        defaultValue="customization"
      >
        {data &&
          Object.keys(data?.loadedActions || {}).map((moduleName) => (
            <Accordion.Item
              key={moduleName}
              value={moduleName}
              sx={{
                background: "#fafafa",
                width: "100%",
                padding: "12px 24px",
                justifyContent: "space-between",
              }}
            >
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Accordion.Control>{moduleName}</Accordion.Control>
                <UnloadModule name={moduleName}></UnloadModule>
              </Box>

              <Accordion.Panel></Accordion.Panel>
            </Accordion.Item>
          ))}
      </Accordion>

      <Stack spacing="xs" my={24}></Stack>
    </>
  );
}

function UnloadModule({ name }) {
  const queryClient = useQueryClient();

  const { mutate: unloadModule, isLoading } = useMutation({
    mutationKey: ["unloadModule"],
    mutationFn: ({ name }: { name: string }) => {
      return client
        .post("/js_admin/actions_unload_module", { name })
        .then((res) => res.data);
    },
    onSuccess: () => queryClient.invalidateQueries(["loadedActions"]),
  });

  return (
    <>
      <Button
        size="xs"
        loading={isLoading}
        onClick={() => unloadModule({ name })}
        sx={{ marginLeft: "12px" }}
        variant="light"
        leftIcon={<IconGitBranchDeleted size={12}></IconGitBranchDeleted>}
      >
        Unload
      </Button>
    </>
  );
}

export default LoadedActions;
