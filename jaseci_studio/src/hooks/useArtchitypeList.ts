import { useQuery } from "@tanstack/react-query";
import { client } from "../components/ReactQuery";
import { Architype } from "./useRegisterArchetype";

function useArchitypeList({ filter }) {
  return useQuery(
    ["architypes", filter],
    () =>
      client
        .post<Architype[]>("/js/architype_list", {
          kind: filter === "all" ? undefined : filter,
          detailed: true,
        })
        .then((res) => res.data),
    {
      onSuccess: (data) => {
        console.log(data);
      },
    }
  );
}

export default useArchitypeList;
