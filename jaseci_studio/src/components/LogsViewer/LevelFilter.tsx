import { Button } from "@mantine/core";
import { useState } from "react";

function LevelFilter() {
  const [filters, setFilters] = useState<Set<"ERROR" | "INFO" | "WARNING">>(
    new Set(Array.from(["ERROR", "WARNING", "INFO"]))
  );

  function addFilter(value: "ERROR" | "INFO" | "WARNING") {
    setFilters((prevState) => new Set(prevState.add(value)));
  }

  function removeFilter(value: "ERROR" | "INFO" | "WARNING") {
    setFilters(
      (prevState) =>
        new Set(Array.from(prevState).filter((level) => level !== value))
    );
  }

  return (
    <Button.Group>
      <Button
        variant="outline"
        size="xs"
        color={filters.has("ERROR") ? "orange" : "gray"}
        onClick={() =>
          filters.has("ERROR") ? removeFilter("ERROR") : addFilter("ERROR")
        }
      >
        Error
      </Button>

      <Button
        variant="outline"
        size="xs"
        color={filters.has("WARNING") ? "orange" : "gray"}
        onClick={() =>
          filters.has("WARNING")
            ? removeFilter("WARNING")
            : addFilter("WARNING")
        }
      >
        Warning
      </Button>
      <Button
        variant="outline"
        size="xs"
        color={filters.has("INFO") ? "orange" : "gray"}
        onClick={() =>
          filters.has("INFO") ? removeFilter("INFO") : addFilter("INFO")
        }
      >
        Info
      </Button>
    </Button.Group>
  );
}

export default LevelFilter;
