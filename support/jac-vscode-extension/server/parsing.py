from .builder import JacAstBuilderSLL
from .utils import debounce
from .server import JacLanguageServer


@debounce(0.5)
def update_doc_tree(ls: JacLanguageServer, doc_uri: str):
    """Update the document tree"""
    doc = ls.workspace.get_document(doc_uri)
    tree = JacAstBuilderSLL(doc.source)
    doc._tree = tree
