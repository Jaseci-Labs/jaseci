import { EditorProps, Monaco } from "@monaco-editor/react";
import { useRef, useState } from "react";
import { jacLang } from "../lib/jacLang";

export function useStudioEditor() {
  const monacoRef = useRef<Monaco | null>(null);
  const [editorValue, setEditorValue] = useState("");

  const handleEditorChange: EditorProps["onChange"] = (value, ev) => {
    setEditorValue(value ?? "");
  };

  function handleEditorBeforeMount(monaco: Monaco) {
    // here is the monaco instance
    // do something before editor is mounted
    // monaco.languages.typescript.javascriptDefaults.setEagerModelSync(true);

    const modelUri = monaco.Uri.parse("inmemory://jac.json"); // a made up unique URI for our model
    const model = monaco.editor.createModel(
      "// write your jac code here",
      "jac",
      modelUri
    );

    model.onDidChangeContent((change) => {
      // reset errors on change
      monaco.editor.getModelMarkers({}).forEach((marker) => {
        if (
          marker.severity === monaco.MarkerSeverity.Error &&
          marker.owner === "jac"
        ) {
          if (
            marker.startLineNumber === change.changes[0].range.startLineNumber
          ) {
            monaco.editor.setModelMarkers(model, "jac", []);
          }
        }
      });
    });

    // monaco.editor.setModelLanguage(model, "jac");
    monaco.languages.register({ id: "jac" });
    monaco.languages.setMonarchTokensProvider("jac", jacLang);
    monaco.editor.setModelLanguage(model, "jac");

    // highlightErrors(model, monaco);

    monacoRef.current = monaco;
  }

  const hideErrors = () => {
    const markers = [];
    const model = monacoRef.current?.editor.getModel(
      "inmemory://jac.json" as any
    );

    monacoRef.current.editor.setModelMarkers(model, "jac", markers);
  };

  const highlightError = ({
    startColumn,
    lineNumber,
    message,
  }: {
    message: string;
    lineNumber: number;
    startColumn: number;
    endColumn: number;
  }) => {
    if (monacoRef.current) {
      const markers = [];
      const model = monacoRef.current?.editor.getModel(
        "inmemory://jac.json" as any
      );

      markers.push({
        severity: monacoRef.current?.MarkerSeverity.Error,
        startLineNumber: lineNumber,
        startColumn: startColumn,
        endLineNumber: lineNumber,
        endColumn: startColumn,
        message: message,
      });

      monacoRef.current.editor.setModelMarkers(model, "jac", markers);
    }
  };

  return {
    handleEditorBeforeMount,
    handleEditorChange,
    highlightError,
    hideErrors,
    editorValue,
  };
}
