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
import io
import os

from mock import Mock
from lsprotocol.types import Position, HoverParams, CompletionParams, Hover
from pygls.server import StdOutTransportAdapter
from pygls.workspace import Document, Workspace
from server.completions import get_builtin_action
from server.utils import update_doc_deps


from ...server import (
    JacLanguageServer,
    JacAstBuilder,
    Diagnostic,
    completions,
    get_doc_errors,
    hover,
    definition,
    DefinitionParams,
    Location,
    # did_close,
    DidOpenTextDocumentParams,
    did_open,
    update_doc_tree,
    # show_configuration_async,
    # show_configuration_callback,
    # show_configuration_thread,
)

doc_path = os.path.join(os.getcwd(), "server/tests/unit/fixtures/main.jac")
with open(doc_path, "r") as f:
    # read the contents of the file
    fake_document_content = f.read()

fake_document_uri = "file://" + doc_path
fake_document = Document(fake_document_uri, fake_document_content)


server = JacLanguageServer("test-jac-server", "v1")
server.publish_diagnostics = Mock()
server.show_message = Mock()
server.show_message_log = Mock()
server.lsp.workspace = Workspace("", None)
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
    # test default completions
    completion_list = completions(
        server,
        CompletionParams(
            text_document=fake_document, position=Position(line=22, character=1)
        ),
    )
    labels = [i.label for i in completion_list.items]

    assert "node" in labels
    assert "walker" in labels
    assert "edge" in labels
    assert "architype" in labels
    assert "import" in labels
    assert "from" in labels


def test_architype_completions():
    _reset_mocks()
    # test completion for a node
    update_doc_tree(server, fake_document_uri)
    update_doc_deps(server, fake_document_uri)

    completion_list = completions(
        server,
        CompletionParams(
            text_document=fake_document, position=Position(line=13, character=41)
        ),
    )
    labels = [i.label for i in completion_list.items]

    assert "house" in labels
    assert "person" in labels
    assert "extra_node" in labels

    # test completion for an edge
    completion_list = completions(
        server,
        CompletionParams(
            text_document=fake_document, position=Position(line=13, character=24)
        ),
    )

    labels = [i.label for i in completion_list.items]

    assert "sample" in labels
    assert "test_edge" in labels
    assert "extra_edge" in labels

    # test completion for a walker
    completion_list = completions(
        server,
        CompletionParams(
            text_document=fake_document, position=Position(line=14, character=30)
        ),
    )

    labels = [i.label for i in completion_list.items]

    assert "count_members" in labels
    assert "init" in labels
    assert "extra_walker" in labels


def test_action_completions():
    """Test completion for built in actions."""
    completion_list = completions(
        server,
        CompletionParams(
            text_document=fake_document, position=Position(line=15, character=12)
        ),
    )
    labels = [i.label for i in completion_list.items]
    assert "log" in labels
    assert "out" in labels
    assert "some_random_fn" not in labels


def test_hover_action():
    """Test hover for built in actions."""
    action_data = get_builtin_action("actload_local", "std")
    hover_data = hover(
        server,
        HoverParams(
            text_document=fake_document, position=Position(line=15, character=13)
        ),
    )

    assert type(hover_data) is Hover
    assert action_data["name"] in hover_data.contents.value
    assert action_data["doc"] in hover_data.contents.value
    assert action_data["args"][0] in hover_data.contents.value


def test_hover_architype():
    """Test hover for architypes."""
    _reset_mocks()
    update_doc_tree(server, fake_document_uri)
    update_doc_deps(server, fake_document_uri)

    # Test hover for a node
    hover_data = hover(
        server,
        HoverParams(
            text_document=fake_document, position=Position(line=13, character=42)
        ),
    )

    assert type(hover_data) is Hover
    assert "house" in hover_data.contents.value
    assert "msg" in hover_data.contents.value

    # Test hover for an edge
    hover_data = hover(
        server,
        HoverParams(
            text_document=fake_document, position=Position(line=13, character=22)
        ),
    )

    assert type(hover_data) is Hover
    assert "test_edge" in hover_data.contents.value
    assert "apple" in hover_data.contents.value

    # Test hover for a walker
    hover_data = hover(
        server,
        HoverParams(
            text_document=fake_document, position=Position(line=14, character=28)
        ),
    )
    assert type(hover_data) is Hover
    assert "extra_walker" in hover_data.contents.value
    assert "a" in hover_data.contents.value
    assert "b" in hover_data.contents.value
    assert "c" in hover_data.contents.value


def test_definition():
    _reset_mocks()
    update_doc_tree(server, fake_document_uri)
    update_doc_deps(server, fake_document_uri)

    # test go to definition for a node
    location = definition(
        server,
        DefinitionParams(
            text_document=fake_document, position=Position(line=13, character=42)
        ),
    )

    assert type(location) is Location
    assert location.uri == fake_document_uri
    assert location.range.start.line == 2
    assert location.range.start.character == 5

    # test go to definition for an edge
    location = definition(
        server,
        DefinitionParams(
            text_document=fake_document, position=Position(line=13, character=22)
        ),
    )

    assert type(location) is Location
    assert location.uri == fake_document_uri
    assert location.range.start.line == 22
    assert location.range.start.character == 5

    # test go to definition for a walker
    location = definition(
        server,
        DefinitionParams(
            text_document=fake_document, position=Position(line=28, character=28)
        ),
    )

    assert type(location) is Location
    assert location.uri == fake_document_uri
    assert location.range.start.line == 19
    assert location.range.start.character == 7

    # test go to definition for a walker in a different file
    location = definition(
        server,
        DefinitionParams(
            text_document=fake_document, position=Position(line=14, character=28)
        ),
    )

    assert type(location) is Location
    assert location.uri == "file://" + os.path.join(
        os.path.dirname(fake_document.path), "extras.jac"
    )
    assert location.range.start.line == 2
    assert location.range.start.character == 7

    # test go to definition for an edge in a different file
    location = definition(
        server,
        DefinitionParams(
            text_document=fake_document, position=Position(line=30, character=16)
        ),
    )

    assert type(location) is Location
    assert location.uri == "file://" + os.path.join(
        os.path.dirname(fake_document.path), "extras.jac"
    )
    assert location.range.start.line == 1
    assert location.range.start.character == 5

    # test go to definition for a node in a different file
    location = definition(
        server,
        DefinitionParams(
            text_document=fake_document, position=Position(line=29, character=33)
        ),
    )

    assert type(location) is Location
    assert location.uri == "file://" + os.path.join(
        os.path.dirname(fake_document.path), "extras.jac"
    )
    assert location.range.start.line == 0
    assert location.range.start.character == 5

    # test go to definition for a import filename
    location = definition(
        server,
        DefinitionParams(
            text_document=fake_document, position=Position(line=0, character=17)
        ),
    )

    assert type(location) is Location
    assert location.uri == "file://" + os.path.join(
        os.path.dirname(fake_document.path), "extras.jac"
    )
    assert location.range.start.line == 0
    assert location.range.start.character == 0


def test_did_open():
    _reset_mocks()
    server.workspace._root_path = os.path.dirname(fake_document.path)
    did_open(server, DidOpenTextDocumentParams(text_document=fake_document))
    doc = server.workspace.get_document(fake_document_uri)

    assert doc is not None
    assert len(doc.symbols) > 0
    assert len(doc.dependencies.keys()) > 0


def test_get_doc_errors():
    _reset_mocks()
    server.workspace._root_path = os.path.dirname(fake_document.path)
    did_open(server, DidOpenTextDocumentParams(text_document=fake_document))
    doc = server.workspace.get_document(fake_document_uri)
    tree = JacAstBuilder(
        mod_name=doc.filename,
        jac_text=doc.source + "\n walke invalid_walker",
        mod_dir=os.path.dirname(doc.path) + "/",
    )
    errors = get_doc_errors(server, doc.uri, tree._parse_errors)
    assert len(errors) > 0
    assert type(errors[0]) is Diagnostic
