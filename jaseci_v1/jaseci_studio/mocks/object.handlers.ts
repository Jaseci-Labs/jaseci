import {
  DefaultRequestMultipartBody,
  MockedRequest,
  rest,
  RestHandler,
} from "msw";
import detailedObject from "./data/detailed_object.json";

export const objectHandlers: Array<
  RestHandler<MockedRequest<DefaultRequestMultipartBody>>
> = [
  rest.post("http://localhost:8500/js/object_get", async (req, res, ctx) => {
    return res(ctx.json(detailedObject));
  }),
];
