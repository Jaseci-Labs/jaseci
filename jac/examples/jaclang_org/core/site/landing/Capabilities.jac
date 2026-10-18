import from "@hugeicons/react" { HugeiconsIcon }
import from "@hugeicons/core-free-icons" {
    FlashIcon,
    SourceCodeIcon,
    SparklesIcon,
    DatabaseIcon,
    CloudServerIcon,
    CheckmarkCircle01Icon
}

glob _KINDS: list[dict[str, any]] = [
         {"name": "Script / CLI tool", "cmd": "jac run app.jac"},
         {"name": "Zero-dependency native binary", "cmd": "jac build --as native"},
         {"name": "REST API + Swagger + auth", "cmd": "jac run --serve api.jac"},
         {"name": "Service apps, one workspace", "cmd": "jac run --serve --fleet"},
         {"name": "Full-stack web app", "cmd": "jac run"},
         {"name": "Desktop app (OS webview)", "cmd": "jac build  # desktop"},
         {"name": "Mobile app (Android / iOS)", "cmd": "jac build  # mobile"},
         {"name": "WebAssembly in the browser", "cmd": "jac build  # web-static"},
         {"name": "AI agents & LLM apps", "cmd": "def act -> Plan by llm();"},
         {"name": "Python package (PyPI wheel)", "cmd": "jac build --as wheel"},
         {"name": "npm package (+ .d.ts)", "cmd": "jac build --as npm"},
         {"name": "C-ABI shared library", "cmd": "jac build --native --lib"},

     ];

def:pub PillarCard(icon: any, title: str, body: str) -> JsxElement;

def:pub Capabilities -> JsxElement;
