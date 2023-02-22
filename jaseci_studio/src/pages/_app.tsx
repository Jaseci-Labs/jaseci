import { AppProps } from "next/app";
import Head from "next/head";
import {
  AppShell,
  Button,
  ColorScheme,
  ColorSchemeProvider,
  Group,
  MantineProvider,
} from "@mantine/core";
import Script from "next/script";
import { theme } from "../../theme";
import ReactQuery from "../components/ReactQuery";
import { NavbarMinimal } from "../components/Navbar";
import { NotificationsProvider } from "@mantine/notifications";
import { SpotlightProvider, openSpotlight } from "@mantine/spotlight";
import type { SpotlightAction } from "@mantine/spotlight";
import { open } from "@tauri-apps/api/shell";

import {
  IconHome,
  IconDashboard,
  IconFileText,
  IconSearch,
  IconCode,
  IconPrompt,
  IconVectorBezierCircle,
  IconHome2,
} from "@tabler/icons";
import { useCallback, useMemo, useState } from "react";
import { useRouter } from "next/router";
import { useHotkeys } from "@mantine/hooks";

const createActions = (
  navigate: (url: string) => void,
  toggleColorScheme: () => void
): SpotlightAction[] => [
  {
    title: "Login",
    description: "Get full information about current system status",
    onTrigger: () => navigate("/"),
    icon: <IconHome2 size={18} />,
  },
  {
    title: "Dashboard",
    description: "Get full information about current system status",
    onTrigger: () => navigate("/dashboard"),
    icon: <IconDashboard size={18} />,
  },
  {
    title: "View Logs",
    description: "Get full information about current system status",
    onTrigger: () => navigate("/logs"),
    icon: <IconPrompt size={18} />,
  },
  {
    title: "Architypes",
    description: "Get full information about current system status",
    onTrigger: () => navigate("/architype"),
    icon: <IconCode size={18} />,
  },
  {
    title: "View Graph",
    description: "View and interact with your graph",
    onTrigger: () => navigate("/graph-viewer"),
    icon: <IconVectorBezierCircle size={18} />,
  },
  {
    title: "Documentation",
    description: "Visit documentation to  learn more about Jaseci",
    onTrigger: () => open("https://docs.jaseci.org"),
    icon: <IconFileText size={18} />,
  },
  {
    title: "Switch Color Scheme",
    description: "Switch between light and dark theme",
    onTrigger: () => toggleColorScheme(),
    icon: <IconFileText size={18} />,
  },
];

export default function App(props: AppProps) {
  const { Component, pageProps } = props;
  const navigate = useRouter().push;
  const [colorScheme, setColorScheme] = useState<ColorScheme>("dark");
  useHotkeys([
    ["mod+L", () => navigate("/logs")],
    ["mod+O", () => navigate("/architype")],
    ["mod+D", () => navigate("/dashboard")],
    ["mod+G", () => navigate("/graph-viewer")],
    ["mod+shift+T", () => toggleColorScheme()],
    ["mod+H", () => navigate("/")],
  ]);

  const toggleColorScheme = useCallback(() => {
    setColorScheme(colorScheme === "dark" ? "light" : "dark");
  }, [colorScheme]);

  const actions = useMemo(
    () => createActions(navigate, toggleColorScheme),
    [colorScheme]
  );

  return (
    <>
      <Head>
        <title>Jaseci Studio</title>
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width"
        />
        <link type={"text/css"} href="ui_kit/components/components.css"></link>
      </Head>
      <script
        type={"module"}
        src={"ui_kit/components/components.esm.js"}
      ></script>
      <script noModule src={"ui_kit/components/components.js"}></script>
      <ReactQuery>
        <MantineProvider
          withGlobalStyles
          withNormalizeCSS
          theme={{ ...theme, colorScheme }}
        >
          <div data-theme="greenheart">
            <AppShell navbar={<NavbarMinimal></NavbarMinimal>}>
              <SpotlightProvider
                actions={actions}
                searchIcon={<IconSearch size={18} />}
                searchPlaceholder="Search..."
                shortcut="mod + k"
                nothingFoundMessage="Nothing found..."
              >
                {/* <SpotlightControl /> */}
              </SpotlightProvider>
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
