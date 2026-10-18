import from "@jac/runtime" { Link }

def matches(p: PackageSummary, q: str) -> bool;

def:pub PackageCard(pkg: PackageSummary) -> JsxElement;

def:pub PackagesIndex(
    catalog: PackageCatalog | None, loading: bool, q: str, onFilter: any
) -> JsxElement;
