import {
  ActionButton,
  Flex,
  Tooltip,
  TooltipTrigger,
  View,
} from "@adobe/react-spectrum";
import GraphBubble from "@spectrum-icons/workflow/GraphBubble";
import Home from "@spectrum-icons/workflow/Home";
import Settings from "@spectrum-icons/workflow/Settings";
import { useAtom } from "jotai";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
// import { isConnectedAtom } from "../atoms/is-conntected.atom";

function Sidebar() {
  const router = useRouter();
  // const [isConnected] = useAtom(isConnectedAtom);

  return (
    <View
      backgroundColor="default"
      borderWidth={"thin"}
      borderStartColor="transparent"
      borderColor="gray-300"
      gridArea="sidebar"
      paddingY="size-160"
    >
      {/* {JSON.stringify(isConnected)} */}
      <Flex
        direction={"column"}
        alignItems="center"
        justifyContent={"space-between"}
        height="100%"
      >
        <Flex alignItems={"center"} direction="column">
          <TooltipTrigger delay={0} placement="end">
            <ActionButton
              onPress={() => router.push("/")}
              aria-label="Go Home"
              isQuiet
            >
              <Home></Home>
            </ActionButton>
            <Tooltip>Home</Tooltip>
          </TooltipTrigger>

          {true && (
            <TooltipTrigger delay={0} placement="end">
              <ActionButton
                onPress={() => router.push("/graph-viewer")}
                aria-label="Graph Viewer"
                isQuiet
              >
                <GraphBubble></GraphBubble>
              </ActionButton>
              <Tooltip>Graph Viewer</Tooltip>
            </TooltipTrigger>
          )}
        </Flex>
        <Flex alignItems={"center"} direction="column">
          <TooltipTrigger delay={0} placement="end">
            <ActionButton
              onPress={() => router.push("/settings")}
              aria-label="Graph Viewer"
              isQuiet
            >
              <Settings></Settings>
            </ActionButton>
            <Tooltip>Settings</Tooltip>
          </TooltipTrigger>
        </Flex>
      </Flex>
    </View>
  );
}

export default Sidebar;
