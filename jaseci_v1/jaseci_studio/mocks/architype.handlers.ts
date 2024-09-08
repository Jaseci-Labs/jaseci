import {
  DefaultRequestMultipartBody,
  MockedRequest,
  rest,
  RestHandler,
} from "msw";
import architypeList from "./data/architype_list.json";
import architypeRegister from "./data/architype_register.json";

export const architypeListHandler: Array<
  RestHandler<MockedRequest<DefaultRequestMultipartBody>>
> = [
  rest.post("http://localhost:8500/js/architype_list", (req, res, ctx) => {
    return res(ctx.json(architypeList));
  }),
  rest.post("http://localhost:8500/js/architype_count", (req, res, ctx) => {
    return res(ctx.json(architypeList.length));
  }),
  rest.post("http://localhost:8500/js/architype_register", (req, res, ctx) => {
    return res(ctx.json(architypeRegister));
  }),
];
