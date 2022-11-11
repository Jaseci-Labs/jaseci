import { Grid, View } from "@adobe/react-spectrum";
import Sidebar from "./Sidebar";

function Layout({ children }) {
  return (
    <Grid
      areas={["header  header", "sidebar content", "footer  footer"]}
      columns={["size-600", "3fr"]}
      rows={["size-500", "1fr"]}
      height="100vh"
    >
      <View backgroundColor="celery-600" gridArea="header" />
      <Sidebar></Sidebar>
      <View backgroundColor="default" padding={"size-160"} gridArea="content">
        {children}
      </View>
    </Grid>
  );
}

export default Layout;
