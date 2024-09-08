import { Button } from "@mantine/core";
import { SetStateAction } from "jotai";
import { Dispatch, useState } from "react";

function LevelFilter({
  level,
  setLevel,
}: {
  level: "ERROR" | "INFO" | "WARNING" | null;
  setLevel: Dispatch<SetStateAction<"ERROR" | "INFO" | "WARNING" | null>>;
}) {
  return (
    <Button.Group>
      <Button
        variant="outline"
        size="xs"
        color={level === "ERROR" ? "orange" : "gray"}
        onClick={() => (level === "ERROR" ? setLevel(null) : setLevel("ERROR"))}
      >
        Error
      </Button>

      <Button
        variant="outline"
        size="xs"
        color={level === "WARNING" ? "orange" : "gray"}
        onClick={() =>
          level === "WARNING" ? setLevel(null) : setLevel("WARNING")
        }
      >
        Warning
      </Button>
      <Button
        variant="outline"
        size="xs"
        color={level === "INFO" ? "orange" : "gray"}
        onClick={() => (level === "INFO" ? setLevel(null) : setLevel("INFO"))}
      >
        Info
      </Button>
    </Button.Group>
  );
}

export default LevelFilter;
