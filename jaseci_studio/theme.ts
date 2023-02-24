import { MantineTheme, DEFAULT_THEME } from "@mantine/core";

export const theme: MantineTheme = {
  ...DEFAULT_THEME,
  primaryColor: "orange",
  globalStyles() {
    return {
      body: {
        // background: "#f8f9fa",
      },
    };
  },
};
