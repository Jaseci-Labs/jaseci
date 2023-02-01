import { showNotification, useNotifications } from "@mantine/notifications";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { client } from "../components/ReactQuery";
import { useStudioEditor } from "./useStudioEditor";

export type Architype = {
  name: string;
  kind: string;
  jid: string;
  j_timestamp: string;
  j_type: string;
  code_sig: string;
  code_ir: string;
};

type SuccessResponse = {
  architype: Architype;
  success: true;
  errors: [];
  stack_trace?: [];
  response: "Successfully created test_architype architype";
};

function useRegisterArchetype(
  highlightError: ReturnType<typeof useStudioEditor>["highlightError"],
  hideErrors: ReturnType<typeof useStudioEditor>["hideErrors"]
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ code, snt }: { code: string; snt: string }) => {
      const base64Code = window.btoa(code);

      return client
        .post<SuccessResponse>(`/js/architype_register`, {
          code: base64Code,
          snt,
          encoded: "true",
        })
        .then((res) => res.data);
    },

    onSuccess(data) {
      queryClient.invalidateQueries(["architypes"]);

      if (data.success) {
        hideErrors();
        showNotification({
          id: "architype-registered",
          title: "Architype registered",
          message: "Your architype has been registered successfully",
          color: "green",
        });
      } else {
        if (data.errors && !data.stack_trace) {
          const ranges = parseErrors(data.errors);
          console.log(ranges);

          ranges.forEach((range) => {
            highlightError({
              lineNumber: range.line,
              message: range.message,
              endColumn: range.column,
              startColumn: range.column,
            });
          });

          // console.log(parseErrors(data.errors));
        }
      }
    },
  });
}

// get line and column numbers from errors
function parseErrors(errors: string[]) {
  const ranges: { line: number; column: number; message: string }[] = [];

  errors.map((error) => {
    const [line, column] = error.split(" ")[2].trim().split(":");
    const message = error.split(" - ")[2];

    ranges.push({ line: Number(line), column: Number(column), message });
  });

  return ranges;
}

export default useRegisterArchetype;
