import MonacoEditor from "@monaco-editor/react";
import { useStudioEditor } from "../hooks/useStudioEditor";

function Editor({ editor }: { editor: ReturnType<typeof useStudioEditor> }) {
  const { editorValue, handleEditorBeforeMount, handleEditorChange } = editor;

  return (
    <>
      <MonacoEditor
        height="100%"
        beforeMount={handleEditorBeforeMount}
        theme="vs-dark"
        onChange={handleEditorChange}
        defaultLanguage="jac"
        defaultPath="inmemory://jac.json"
      />
    </>
  );
}

export default Editor;
