import from core.site.docs.DocsShell { DocsShell }

def:pub page -> JsxPage;

impl page -> JsxPage {
    return <DocsShell/>;
}
