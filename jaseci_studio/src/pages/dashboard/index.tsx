import { Box, Card, Flex, Grid } from "@mantine/core";
import { getCookie } from "cookies-next";
import BasicSummary from "../../components/BasicSummary";

export const getServerSideProps = ({ req, res }) => {
  const tokenCookieResult = getCookie("token", { req, res }) || null;
  const serverUrl = getCookie("serverUrl", { req, res }) || null;

  return { props: { serverUrl, tokenCookieResult } };
};

function Dashboard({ serverUrl, tokenCookieResult }) {
  return (
    <Box>
      <>{JSON.stringify({ serverUrl, tokenCookieResult })}</>
      <Grid columns={3}>
        <Grid.Col span={1}>
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
  );
}

export default Dashboard;
