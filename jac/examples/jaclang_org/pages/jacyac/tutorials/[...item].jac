import from core.site.jacyac.JacYac { JacYac }

def:pub page -> JsxPage;

impl page -> JsxPage {
    return
        <div className="pt-16">
            <JacYac initialTab="tutorials"/>
        </div>;
}
