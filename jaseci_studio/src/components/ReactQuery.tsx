import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import axios from "axios";
import { getCookie } from "cookies-next";
import { redirect } from "next/navigation";
import { NextRouter } from "next/router";
import { ReactNode } from "react";

export const client = axios.create();

client.interceptors.request.use(
  function (request) {
    const token = getCookie("token");
    const serverUrl = getCookie("serverUrl");

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
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export default ReactQuery;
