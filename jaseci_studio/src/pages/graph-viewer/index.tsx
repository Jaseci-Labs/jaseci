import { Card, Flex, Title } from "@mantine/core";

function GraphViewerPage() {
  return (
    <>
      <Flex justify={"center"}>
        <Card
          w="100%"
          h="100%"
          withBorder
          shadow={"md"}
          p={8}
          radius={"md"}
          sx={{ margin: "0 auto" }}
        >
          <Title order={3} mb={"xl"}>
            Graph
          </Title>

          <jsc-graph
            height="85vh"
            serverUrl="http://localhost:8888"
          ></jsc-graph>
        </Card>
      </Flex>
    </>
  );
}

export default GraphViewerPage;

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "jsc-graph": { height: string; serverUrl: string };
    }
  }
}
