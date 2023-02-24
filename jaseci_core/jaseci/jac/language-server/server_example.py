from antlr4 import *
from pygls import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.InputStream import InputStream
from antlr4.CommonTokenStream import CommonTokenStream
from jaseci.jac.jac_parse import jacLexer, jacParser
from lspprotocol.types import *


from pygls.server import LanguageServer
from pygls.features import (
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_COMPLETION,
)


class PythonServer(LanguageServer):
    def __init__(self):
        super().__init__()

        self.workspace = {}

    def get_tokens(self, source):
        input_stream = InputStream(source)
        lexer = jacLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = jacParser(stream)
        parser.removeErrorListeners()
        tree = parser.file_input()
        return tree

    # def diagnose(self, doc_uri):
    #     doc = self.workspace[doc_uri]
    #     errors = []
    #     source = doc.text
    #     tree = self.get_tokens(source)
    #     for error in tree.parser_errors:
    #         line, col = error.line, error.col
    #         message = error.message
    #         diagnostic = Diagnostic(
    #             range=Range(
    #                 start=Position(line=line, character=col),
    #                 end=Position(line=line, character=col + 1),
    #             ),
    #             message=message,
    #             severity=DiagnosticSeverity.Error,
    #         )
    #         errors.append(diagnostic)
    #     return errors

    def on_initialize(self, params: InitializeParams) -> InitializeResult:
        return InitializeResult(
            capabilities={
                "textDocumentSync": TextDocumentSyncKind.Full,
                "completionProvider": {
                    "resolveProvider": False,
                    "triggerCharacters": ["."],
                },
            }
        )

    def on_text_document_did_open(self, text_document: TextDocumentItem):
        self.workspace[text_document.uri] = text_document

        diagnostics = self.diagnose(text_document.uri)

        self.publish_diagnostics(text_document.uri, diagnostics)

    def on_text_document_did_change(self, text_document: TextDocumentItem):
        self.workspace[text_document.uri] = text_document

        diagnostics = self.diagnose(text_document.uri)

        self.publish_diagnostics(text_document.uri, diagnostics)

    def on_text_document_completion(
        self, text_document: TextDocumentItem, position: Position
    ):
        source = text_document.text
        line = position.line + 1


server.start_tcp("127.0.0.1:8080")
