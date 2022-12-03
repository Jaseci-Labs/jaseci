import {
  DefaultRequestMultipartBody,
  MockedRequest,
  rest,
  RestHandler,
} from "msw";
import exampleLogs from "./data/logger_get.json";

export const logsHandler: Array<
  RestHandler<MockedRequest<DefaultRequestMultipartBody>>
> = [
  rest.post("http://mysite.com/js_admin/logger_get", (req, res, ctx) => {
    return res(ctx.json(exampleLogs));
  }),
];
