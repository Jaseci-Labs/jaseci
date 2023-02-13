import { AppProps } from "next/app";
import Head from "next/head";
import { AppShell, MantineProvider } from "@mantine/core";
import Script from "next/script";
import { theme } from "../../theme";
import ReactQuery from "../components/ReactQuery";
import { NavbarMinimal } from "../components/Navbar";
import { NotificationsProvider } from "@mantine/notifications";

export default function App(props: AppProps) {
  const { Component, pageProps } = props;

  return (
    <>
      <Head>
        <title>Jaseci Studio</title>
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width"
        />
        <link type={"text/css"} href="/ui_kit/components/components.css"></link>
      </Head>
      <Script
        type={"module"}
        src={"/ui_kit/components/components.esm.js"}
      ></Script>
      <Script noModule src={"/ui_kit/components/components.js"}></Script>
      <ReactQuery>
        <MantineProvider withGlobalStyles withNormalizeCSS theme={theme}>
          <div data-theme="greenheart">
            <AppShell navbar={<NavbarMinimal></NavbarMinimal>}>
              <NotificationsProvider>
                <Component {...pageProps} />
              </NotificationsProvider>
            </AppShell>
          </div>
        </MantineProvider>
      </ReactQuery>
    </>
  );
}
