import { Box, Card, Flex, Grid } from "@mantine/core";
import Head from "next/head";
import BasicSummary from "../../components/BasicSummary";

function Dashboard() {
  return (
    <>
      <Head>
        <title>Dashboard</title>
      </Head>

      <Box>
        <Grid columns={3}>
          <Grid.Col span={2}>
            <BasicSummary></BasicSummary>
          </Grid.Col>
          <Grid.Col span={1}>
            <Card
              withBorder
              shadow={"md"}
              p={30}
              radius={"md"}
              sx={{ margin: "0 auto" }}
            >
              <Flex justify={"space-between"}></Flex>
            </Card>
          </Grid.Col>
          <Grid.Col span={1}>
            <Card
              withBorder
              shadow={"md"}
              p={30}
              radius={"md"}
              sx={{ margin: "0 auto" }}
            >
              <Flex justify={"space-between"}></Flex>
            </Card>
          </Grid.Col>
        </Grid>
      </Box>
    </>
  );
}

export default Dashboard;
