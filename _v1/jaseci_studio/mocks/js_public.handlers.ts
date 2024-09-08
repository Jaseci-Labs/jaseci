import {
  DefaultRequestMultipartBody,
  MockedRequest,
  rest,
  RestHandler,
} from "msw";

const publicInfo = {
  Version: "1.4.0.6",
  Creator: "Jason Mars and friends",
  URL: "https://jaseci.org",
};

export const jsPublicHandler: Array<
  RestHandler<MockedRequest<DefaultRequestMultipartBody>>
> = [
  rest.post("http://localhost:8500/js_public/info", (req, res, ctx) => {
    return res(ctx.json(publicInfo));
  }),
];
