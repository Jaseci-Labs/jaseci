import {
  DefaultRequestMultipartBody,
  MockedRequest,
  rest,
  RestHandler,
} from "msw";

export const walkerHandlers: Array<
  RestHandler<MockedRequest<DefaultRequestMultipartBody>>
> = [
  rest.post("http://localhost:8500/js/walker_run", (req, res, ctx) => {
    return res(
      ctx.json({
        success: true,
        report: [],
        final_node: "urn:uuid:7bccb142-e552-4f1e-9026-c30cd3af6be6",
        yielded: false,
      })
    );
  }),
];
