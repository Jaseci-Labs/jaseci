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

async function getPythonPath() {
  const extension = extensions.getExtension("ms-python.python");
  if (!extension.isActive) {
    await extension.activate();
  }

  if (!extension) {
    return;
  }

  const pythonPath =
    extension.exports.settings.getExecutionDetails().execCommand;
  if (!pythonPath) {
    return;
  }

  return pythonPath;
}

export async function activate(context: ExtensionContext): Promise<void> {
  if (context.extensionMode === ExtensionMode.Development) {
    // Development - Run the server manually
    const path = await getPythonPath();
    client = startLangServerTCP(2087);
    window.showInformationMessage(`Python path: ${path}`);
  } else {
    const cwd = path.join(__dirname, "..", "..");
    const workspaceConfig = workspace.getConfiguration("jac");

    let pythonPath = workspaceConfig.get<string>("pythonPath");

    if (!pythonPath) {
      // get python path from python extension
      pythonPath = await getPythonPath();
    }

    if (!pythonPath) {
      window.showErrorMessage(
        "Unable to start the jac language server. \n Select a Python interpreter first where Jaseci is installed."
      );

      throw new Error("`jac.pythonPath` is not set");
    }

    client = startLangServer(pythonPath, ["-m", "server"], cwd);
  }

  context.subscriptions.push(client.start() as any);
}

export function deactivate(): Thenable<void> {
  console.log("JAC ext deactivated!");
  return client ? client.stop() : Promise.resolve();
}
You need to sthethamatcs'ation location