import { useQuery } from "@tanstack/react-query";
import { client } from "../components/ReactQuery";

type UserInfo = {
  id: number;
  email: string;
  name: string;
  is_activated: boolean;
  is_superuser: boolean;
};

function useUserInfo() {
  return useQuery(["userInfo"], async () => {
    const response = await client.get<UserInfo>("/user/manage");
    return response.data;
  });
}

export default useUserInfo;
