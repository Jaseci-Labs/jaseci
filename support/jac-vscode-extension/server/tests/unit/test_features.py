############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import asyncio
import io
import json
import threading
import time

import pytest
from mock import Mock
from lsprotocol.types import (DidCloseTextDocumentParams,
                              DidOpenTextDocumentParams, TextDocumentIdentifier,
                              WorkspaceConfigurationResponse,
                              TextDocumentItem)
from pygls.server import StdOutTransportAdapter
from pygls.workspace import Document, Workspace

from ...server import (
    JsonLanguageServer,
    completions,
    did_close,
    did_open,
    show_configuration_async,
    show_configuration_callback,
    show_configuration_thread,
)

fake_document_uri = 'file://fake_doc.txt'
fake_document_content = 'text'
fake_document = Document(fake_document_uri, fake_document_content)


server = JsonLanguageServer('test-json-server', 'v1')
server.publish_diagnostics = Mock()
server.show_message = Mock()
server.show_message_log = Mock()
server.lsp.workspace = Workspace('', None)
server.lsp._send_only_body = True
server.workspace.get_document = Mock(return_value=fake_document)


def _reset_mocks(stdin=None, stdout=None):

    stdin = stdin or io.StringIO()
    stdout = stdout or io.StringIO()

    server.lsp.transport = StdOutTransportAdapter(stdin, stdout)
    server.publish_diagnostics.reset_mock()
    server.show_message.reset_mock()
    server.show_message_log.reset_mock()


def test_completions():
    completion_list = completions()
    labels = [i.label for i in completion_list.items]

    assert '"' in labels
    assert '[' in labels
    assert ']' in labels
    assert '{' in labels
    assert '}' in labels


def test_did_close():
    _reset_mocks()

    params = DidCloseTextDocumentParams(
        text_document=TextDocumentIdentifier(uri=fake_document_uri))

    did_close(server, params)

    # Check if show message is called
    server.show_message.assert_called_once()


@pytest.mark.asyncio
async def test_did_open():
    _reset_mocks()

    expected_msg = None

    # Get expected error message
    try:
        json.loads(fake_document_content)
    except json.JSONDecodeError as err:
        expected_msg = err.msg

    params = DidOpenTextDocumentParams(
        text_document=TextDocumentItem(uri=fake_document_uri,
                                       language_id='json',
                                       version=1,
                                       text=fake_document_content))

    await did_open(server, params)

    # Check publish diagnostics is called
    server.publish_diagnostics.assert_called_once()

    # Check publish diagnostics args message
    args = server.publish_diagnostics.call_args
    assert args[0][1][0].message is expected_msg

    # Check other methods are called
    server.show_message.assert_called_once()
    server.show_message_log.assert_called_once()


def test_show_configuration_callback():
    stdout = io.StringIO()
    _reset_mocks(stdout=stdout)

    show_configuration_callback(server)

    # Grab the request id
    id_ = json.loads(stdout.getvalue())['id']

    # Simulate the client response
    server.lsp._procedure_handler(
        WorkspaceConfigurationResponse(
            id=id_,
            result=[
                {'exampleConfiguration': 'some_value'}
            ]
        )
    )

    server.show_message.assert_called_with(
        f'jsonServer.exampleConfiguration value: some_value'
    )


@pytest.mark.asyncio
async def test_show_configuration_async():
    stdout = io.StringIO()
    _reset_mocks(stdout=stdout)

    async def send_response():
        await asyncio.sleep(0.1)

        # Grab the request id
        id_ = json.loads(stdout.getvalue())['id']

        # Simulate the client response
        server.lsp._procedure_handler(
            WorkspaceConfigurationResponse(
                id=id_,
                result=[
                    {"exampleConfiguration": "some_value"}
                ]
            )
        )

    await asyncio.gather(
        show_configuration_async(server),
        send_response()
    )

    server.show_message.assert_called_with(
        f'jsonServer.exampleConfiguration value: some_value'
    )


def test_show_configuration_thread():
    stdout = io.StringIO()
    _reset_mocks(stdout=stdout)

    thread = threading.Thread(
        target=show_configuration_thread,
        args=(server,),
    )
    thread.start()
    time.sleep(1)

    # Grab the request id
    id_ = json.loads(stdout.getvalue())['id']

    # Simulate the client response
    server.lsp._procedure_handler(
        WorkspaceConfigurationResponse(
            id=id_,
            result=[
                {'exampleConfiguration': 'some_value'}
            ]
        )
    )

    thread.join()

    server.show_message.assert_called_with(
        f'jsonServer.exampleConfiguration value: some_value'
    )
