import { Card, Flex } from "@mantine/core";

function GraphViewerPage() {
  return (
    <>
      <Flex justify={"center"} align="center">
        <Card
          w="90%"
          h="800px"
          withBorder
          shadow={"md"}
          p={30}
          radius={"md"}
          sx={{ margin: "0 auto" }}
        >
          <jsc-graph
            height="80vh"
            serverUrl="http://localhost:6000"
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
