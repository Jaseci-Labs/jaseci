import { AppShell } from "@mantine/core";
import { NavbarMinimal } from "../components/Navbar";
import ReactQuery from "../components/ReactQuery";
import RootStyleRegistry from "./emotion";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <head></head>
      <body>
        <RootStyleRegistry>
          <ReactQuery>
            <div data-theme="greenheart">
              <AppShell navbar={<NavbarMinimal></NavbarMinimal>}>
                {children}
              </AppShell>
            </div>
          </ReactQuery>
        </RootStyleRegistry>
      </body>
    </html>
  );
}
