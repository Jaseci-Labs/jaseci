import { useMutation, useQuery } from "@tanstack/react-query";
import { client } from "../components/ReactQuery";

function useRunWalker() {
  return useMutation({
    mutationFn: async (data?: {
      payload?: Record<string, any>;
      walker: string;
      nd?: string;
    }) => {
      const result = await client.post(
        "/js/walker_run",
        { name: data.walker, nd: data.nd, ctx: { ...(data.payload || {}) } } ||
          {}
      );

      return result.data;
    },
  });
}

export default useRunWalker;
