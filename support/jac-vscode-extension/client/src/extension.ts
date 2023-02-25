/* -------------------------------------------------------------------------
 * Original work Copyright (c) Microsoft Corporation. All rights reserved.
 * Original work licensed under the MIT License.
 * See ThirdPartyNotices.txt in the project root for license information.
 * All modifications Copyright (c) Open Law Library. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http: // www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ----------------------------------------------------------------------- */
"use strict";

import * as net from "net";
import * as path from "path";
import {
  ExtensionContext,
  ExtensionMode,
  workspace,
  window,
  extensions,
  ConfigurationTarget,
  Uri,
} from "vscode";
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
} from "vscode-languageclient/node";

let client: LanguageClient;

function getClientOptions(): LanguageClientOptions {
  return {
    // Register the server for plain text documents
    documentSelector: [
      { scheme: "file", language: "jac" },
      { scheme: "untitled", language: "jac" },
    ],
    outputChannelName: "[jac] JacLanguageServer",
    synchronize: {
      // Notify the server about file changes to '.clientrc files contain in the workspace
      fileEvents: workspace.createFileSystemWatcher("**/.clientrc"),
    },
  };
}

function startLangServerTCP(addr: number): LanguageClient {
  const serverOptions: ServerOptions = () => {
    return new Promise((resolve /*, reject */) => {
      const clientSocket = new net.Socket();
      clientSocket.connect(addr, "127.0.0.1", () => {
        resolve({
          reader: clientSocket,
          writer: clientSocket,
        });
      });
    });
  };

  return new LanguageClient(
    `tcp lang server (port ${addr})`,
    serverOptions,
    getClientOptions()
  );
}

function startLangServer(
  command: string,
  args: string[],
  cwd: string
): LanguageClient {
  const serverOptions: ServerOptions = {
    args,
    command,
    options: { cwd },
  };

  return new LanguageClient(command, serverOptions, getClientOptions());
}

export function activate(context: ExtensionContext): void {
  if (context.extensionMode === ExtensionMode.Development) {
    // Development - Run the server manually
    client = startLangServerTCP(2087);
  } else {
    // Production - Client is going to run the server (for use within `.vsix` package)
    const cwd = path.join(__dirname, "..", "..");
    const workspaceConfig = workspace.getConfiguration("jac");

    const pythonPath = workspaceConfig.get<string>("pythonPath");

    if (!pythonPath) {
      window.showErrorMessage(
        "Unable to start the jac language server. \n Select a Python interpreter first where Jaseci is installed.",
        "Select Python Interpreter",
        "Cancel"
      );
      // .then((selection) => {
      //   if (selection === "Select Python Interpreter") {
      //     const options = {
      //       placeHolder: "Select Python Interpreter",
      //       matchOnDescription: true,
      //       matchOnDetail: true,
      //     };

      //     const workspaceFolder = workspace.workspaceFolders[0];

      //     window
      //       .showQuickPick(
      //         extensions
      //           .getExtension("ms-python.python")
      //           .exports.getInterpreterDetails(workspaceFolder.uri),
      //         options
      //       )
      //       .then((selected) => {
      //         if (selected) {
      //           workspaceConfig.update(
      //             "pythonPath",
      //             selected,
      //             ConfigurationTarget.Workspace
      //           );
      //         }
      //       });
      //   }

      throw new Error("`jacServer.pythonPath` is not set");
      // });
    }

    client = startLangServer(pythonPath, ["-m", "server"], cwd);
  }

  context.subscriptions.push(client.start());
}

export function deactivate(): Thenable<void> {
  return client ? client.stop() : Promise.resolve();
}
