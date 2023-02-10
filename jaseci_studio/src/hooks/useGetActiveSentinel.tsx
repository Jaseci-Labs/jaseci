import { useQuery } from "@tanstack/react-query";
import { client } from "../components/ReactQuery";

type SuccessResponse = {
  version: null;
  name: string;
  kind: string;
  jid: string;
  j_timestamp: string;
  j_type: string;
  code_sig: string;
};

export function getActiveSentinel() {
  return useQuery({
    queryKey: ["activeSentinel"],
    queryFn: () => {
      return client
        .post<SuccessResponse>("/js/sentinel_active_get")
        .then((res) => res.data);
    },
  });
}
