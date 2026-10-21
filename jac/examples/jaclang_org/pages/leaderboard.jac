import from "@jac/runtime" { Navigate }

def:pub page -> JsxPage;

impl page -> JsxPage {
    return <Navigate to="/jacyac" replace={True}/>;
}
