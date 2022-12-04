import { loginHandlers } from "./login.handlers";
import { logsHandler } from "./logs.handlers";

export default [...loginHandlers, ...logsHandler];
