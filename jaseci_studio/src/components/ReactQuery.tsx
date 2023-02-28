import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import axios from "axios";
import { usePathname, useRouter } from "next/navigation";
import { ReactNode, useEffect } from "react";

export const client = axios.create();

client.interceptors.request.use(
  function (request) {
    const token = localStorage.getItem("token");
    const serverUrl = localStorage.getItem("serverUrl");

    if (process.env.NODE_ENV === "test") {
      return {
        ...request,
        baseURL: "http://localhost:8500",
        headers: {
          Authorization: `token ${token}`,
        },
      };
    }

    if (serverUrl && token) {
      return {
        ...request,
        baseURL: serverUrl as string,
        headers: {
          Authorization: `token ${token}`,
        },
      };
    }

    return request;
  },
  function (error) {
    return Promise.reject(error);
  }
);

const queryClient = new QueryClient();

function ReactQuery({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const serverUrl = localStorage.getItem("serverUrl");

    if ((!token || !serverUrl) && pathname !== "/") {
      router.push("/");
      localStorage.clear();
    }
  }, [pathname]);

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export default ReactQuery;
