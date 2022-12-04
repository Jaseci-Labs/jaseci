import { Card, Table, useMantineTheme } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { client } from "../ReactQuery";
import { parse, bgYellow } from "ansicolor";
import { NextFont } from "@next/font/dist/types";

type ServerLog = {
  log: string;
  date: string;
  level: "INFO" | "ERROR" | "WARNING";
};

function LogsViewer({
  font,
  searchTerm = "",
}: {
  font: NextFont;
  searchTerm: string;
}) {
  const theme = useMantineTheme();
  const { data } = useQuery({
    queryKey: [searchTerm ? `logs-${searchTerm}` : "logs"],
    queryFn: async () => {
      return client
        .post<ServerLog[]>("/js_admin/logger_get", { search: searchTerm })
        .then((res) => res.data);
    },
    refetchInterval: 15000,
    initialData: [],
  });

  return (
    <Card
      sx={{
        background: "#FAFAFA",
        height: "500px",
        overflow: "auto",
        textRendering: "optimizeLegibility",
      }}
    >
      {Array.isArray(data) &&
        data?.map((serverLog, index) => (
          <Table
            key={
              serverLog.date + index || "" + new Date().toISOString() + index
            }
            fontSize="xs"
            striped
            highlightOnHover
            sx={{ wordBreak: "break-word", fontFamily: "monospace" }}
            withBorder
          >
            <tbody>
              <tr
                className={font.className}
                style={{
                  background:
                    serverLog.level === "ERROR"
                      ? theme.colors.pink[1]
                      : undefined,
                }}
              >
                <td style={{ width: "110px" }}>
                  {serverLog.date?.split(" ")[0] || "Date Unknown"}
                  <br />
                  <span
                    style={{
                      color: theme.colors.gray[8],
                      fontSize: theme.fontSizes.xs,
                    }}
                  >
                    {/* Render Time */}
                    {serverLog.date &&
                      serverLog.date?.split(" ")[1]?.replace(",", ".")}
                  </span>
                </td>

                <td>
                  {/* Get ansi colors and highlight instances of the search query in the log */}
                  {parse(
                    serverLog.log
                      .replace(serverLog.date + " - ", "")
                      .replaceAll(searchTerm || null, bgYellow(searchTerm))
                  )?.spans?.map((span, index) => (
                    <span
                      key={span.text + index}
                      style={{
                        background: span.bgColor?.name,
                        fontWeight: span.bold ? "bold" : undefined,
                        color:
                          span.color?.name === "yellow"
                            ? "blue"
                            : span.color?.name,
                      }}
                    >
                      {span.text}
                    </span>
                  ))}
                </td>
              </tr>
            </tbody>
          </Table>
        ))}
    </Card>
  );
}

export default LogsViewer;
