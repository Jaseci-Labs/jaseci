import {
  DefaultRequestMultipartBody,
  MockedRequest,
  rest,
  RestHandler,
} from "msw";

export const loginHandlers: Array<
  RestHandler<MockedRequest<DefaultRequestMultipartBody>>
> = [
  rest.post("http://mysite.com/user/token/", (req, res, ctx) => {
    return res(
      ctx.json({
        token: "abcde",
      })
    );
  }),
  rest.get("http://localhost:8005/user/manage/", (req, res, ctx) => {
    return res(
      ctx.json({
        token: "abcde",
        is_activated: true,
        is_superuser: true,
      })
    );
  }),
];
