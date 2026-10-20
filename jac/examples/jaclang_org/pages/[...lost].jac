import from core.site.ui.NotFound { NotFound }

def:pub page -> JsxPage;

impl page -> JsxPage {
    return <NotFound/>;
}
