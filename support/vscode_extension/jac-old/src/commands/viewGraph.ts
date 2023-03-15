import * as vscode from "vscode";
import { getGraphWebviewContent } from "../views/viewGraphWebview";

export default async function viewGraph() {
  try {
    vscode.window.showQuickPick(["Right", "Left"]);
    const activeDocument = vscode.window.activeTextEditor?.document;
    const documentText = activeDocument?.getText();
    const hppc = await import("@hpcc-js/wasm").catch((err) =>
      console.log("Unable to import graphviz")
    );
    const svg = await hppc?.graphviz.layout(
      documentText as string,
      "svg",
      "dot"
    );
    // create a webview to the right of the content
    const panel = vscode.window.createWebviewPanel(
      "jacGraph",
      "Jac Graph",
      vscode.ViewColumn.Two
    );

    console.log({ svg });

    panel.webview.html = getGraphWebviewContent(
      svg || "<p>Unable to generate graph</p>"
    );
  } catch (err) {
    console.log(err);
  }
}
