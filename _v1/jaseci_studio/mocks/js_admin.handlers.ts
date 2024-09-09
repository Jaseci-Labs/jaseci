import {
  DefaultRequestMultipartBody,
  MockedRequest,
  rest,
  RestHandler,
} from "msw";
import allUsers from "./data/master_allusers.json";

export const jsAdminHandler: Array<
  RestHandler<MockedRequest<DefaultRequestMultipartBody>>
> = [
  rest.post(
    "http://localhost:8500/js_admin/master_allusers",
    async (req, res, ctx) => {
      return res(ctx.json(allUsers));
    }
  ),
];
