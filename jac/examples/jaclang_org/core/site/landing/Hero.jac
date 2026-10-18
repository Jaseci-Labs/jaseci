import from "@jac/runtime" { Link }

import from "@hugeicons/react" { HugeiconsIcon }
import from "@hugeicons/core-free-icons" { StarIcon, BookOpen01Icon }

glob INSTALL_CMD: str = "curl -fsSL https://jaclang.org/install.sh | bash";

def:pub Hero -> JsxElement;
