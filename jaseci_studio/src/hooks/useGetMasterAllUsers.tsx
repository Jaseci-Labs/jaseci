import { useQuery } from "@tanstack/react-query";
import { client } from "../components/ReactQuery";

type User = {
  id: number;
  user: string;
  jid: string;
  name: string;
  created_date: string;
  is_activated: boolean;
  is_superuser: boolean;
};

export const useGetMasterAllUsers = ({
  search,
  offset,
}: {
  search: string;
  offset: number;
  limit: number;
}) => {
  let LIMIT = 1;

  return useQuery(["master_allusers", search, offset], async () => {
    const response = await client.post<{ data: User[]; total: number }>(
      "/js_admin/master_allusers",
      { search, offset, limit: LIMIT }
    );

    return response.data;
  });
};
