import { Text, Card, Title, Grid } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { client } from "./ReactQuery";

function BasicSummary() {
  const { data } = useQuery({
    queryKey: ["architypeSummary"],
    queryFn: () => {
      return Promise.all([
        client
          .post("/js/architype_count", { kind: "node" })
          .then((res) => res.data),
        client
          .post("/js/architype_count", { kind: "edge" })
          .then((res) => res.data),
        client
          .post("/js/architype_count", { kind: "walker" })
          .then((res) => res.data),
        client
          .post("/js/architype_count", { kind: "graph" })
          .then((res) => res.data),
      ]).then((value) => ({
        totalNodes: value[0],
        totalEdges: value[1],
        totalWalkers: value[2],
        totalGraphs: value[3],
      }));
    },
    placeholderData: {
      totalEdges: 0,
      totalNodes: 0,
      totalWalkers: 0,
      totalGraphs: 0,
    },
  });

  return (
    <Card
      withBorder
      shadow={"md"}
      p={30}
      radius={"md"}
      sx={{ margin: "0 auto" }}
    >
      <Title order={3} mb="lg">
        Summary
      </Title>
      <Grid columns={4}>
        <Grid.Col span={1}>
          <Title order={5} aria-label="Total Nodes">
            <>
              {data?.totalNodes} <br />
              <Text component="span" weight={"normal"} color="dimmed">
                Nodes
              </Text>
            </>
          </Title>
        </Grid.Col>
        <Grid.Col span={1}>
          <Title order={5} aria-label="Total Walkers">
            {data?.totalWalkers} <br></br>
            <Text weight={"normal"} component="span" color="dimmed">
              Walkers
            </Text>
          </Title>
        </Grid.Col>
        <Grid.Col span={1}>
          <Title order={5} aria-label="Total Edges">
            {data?.totalEdges} <br />
            <Text weight={"normal"} component="span" color="dimmed">
              Edges
            </Text>
          </Title>
        </Grid.Col>
        <Grid.Col span={1}>
          <Title order={5} aria-label="Total Graphs">
            {data?.totalGraphs} <br />
            <Text weight={"normal"} component="span" color="dimmed">
              Graphs
            </Text>
          </Title>
        </Grid.Col>
      </Grid>
    </Card>
  );
}

export default BasicSummary;
