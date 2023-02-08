import { architypeListHandler } from "./architype.handlers";
import { jsPublicHandler } from "./js_public.handlers";
import { loginHandlers } from "./login.handlers";
import { logsHandler } from "./logs.handlers";

export default [
  ...loginHandlers,
  ...logsHandler,
  ...architypeListHandler,
  ...jsPublicHandler,
];
