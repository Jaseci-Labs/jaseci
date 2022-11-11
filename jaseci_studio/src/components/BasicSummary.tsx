import { Text, Card, Title, Grid } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";

function BasicSummary() {
  const { isLoading, data } = useQuery({
    queryFn: () => {
      const token = localStorage.getItem("token");
      return Promise.all([
        fetch("http://localhost:8200/js/node_total", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
            Authorization: "token " + token,
          },
        }).then((res) => res.json()),
        fetch("http://localhost:8200/js/edge_total", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
            Authorization: "token " + token,
          },
        }).then((res) => res.json()),
        fetch("http://localhost:8200/js/walker_total", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
            Authorization: "token " + token,
          },
        }).then((res) => res.json()),
      ]).then((value) => ({
        totalNodes: value[0],
        totalEdges: value[1],
        totalWalkers: value[2],
      }));
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
      <Grid columns={3}>
        <Grid.Col span={1}>
          <Title order={5}>
            {data?.totalNodes} <br></br>
            <Text component="span" weight={"normal"} color="dimmed">
              Nodes
            </Text>
          </Title>
        </Grid.Col>
        <Grid.Col span={1}>
          <Title order={5}>
            {data?.totalWalkers} <br></br>
            <Text weight={"normal"} component="span" color="dimmed">
              Walkers
            </Text>
          </Title>
        </Grid.Col>
        <Grid.Col span={1}>
          <Title order={5}>
            {data?.totalEdges} <br />
            <Text weight={"normal"} component="span" color="dimmed">
              Edges
            </Text>
          </Title>
        </Grid.Col>
      </Grid>
    </Card>
  );
}

export default BasicSummary;
