import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { ReactNode } from "react";
const queryClient = new QueryClient();

function ReactQuery({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export default ReactQuery;
