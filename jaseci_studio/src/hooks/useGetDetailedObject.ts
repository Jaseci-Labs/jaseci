import { useMutation } from "@tanstack/react-query";
import { client } from "../components/ReactQuery";

type DetailedUserObject = {
  name: string;
  kind: string;
  jid: string;
  j_timestamp: string;
  j_type: string;
  j_parent: string;
  j_master: string;
  j_access: string;
  j_r_acc_ids: string[];
  j_rw_acc_ids: string[];
  caller: string;
  head_master_id: string;
  sub_master_ids: string[];
  alias_map: {};
  perm_default: string;
  active_gph_id: string;
  graph_ids: string[];
  spawned_walker_ids: string[];
  yielded_walkers_ids: string[];
  active_snt_id: string;
  sentinel_ids: string[];
};

export const useGetDetailedObject = () => {
  return useMutation(async (jid: string) => {
    const response = await client.post<DetailedUserObject>("/js/object_get", {
      obj: jid,
      detailed: true,
    });

    return response.data;
  });
};
