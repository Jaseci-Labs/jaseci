import { atom } from "jotai";

const isConnectedAtom = atom(localStorage.getItem("token") ?? "foo");
