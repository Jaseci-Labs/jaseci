import { architypeListHandler } from "./architype.handlers";
import { jsAdminHandler } from "./js_admin.handlers";
import { jsPublicHandler } from "./js_public.handlers";
import { loginHandlers } from "./login.handlers";
import { logsHandler } from "./logs.handlers";
import { objectHandlers } from "./object.handlers";

export default [
  ...loginHandlers,
  ...logsHandler,
  ...architypeListHandler,
  ...jsPublicHandler,
  ...jsAdminHandler,
  ...objectHandlers,
];
