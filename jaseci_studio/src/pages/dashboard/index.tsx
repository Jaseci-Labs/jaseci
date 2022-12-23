import { Box, Card, Flex, Grid, Title } from "@mantine/core";
import Head from "next/head";
import BasicSummary from "../../components/BasicSummary";
import ServerInfo from "../../components/ServerInfo";

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
            <ServerInfo></ServerInfo>
          </Grid.Col>
        </Grid>
      </Box>
    </>
  );
}

export default Dashboard;
