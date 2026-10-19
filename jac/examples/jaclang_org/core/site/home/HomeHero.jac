import from "@jac/runtime" { Link }

glob HOME_INSTALL: str = "curl -fsSL https://jaclang.org/install.sh | bash",
     _PILLARS: list[dict[str, str]] = [
         {
             "num": "01",
             "id": "one-language",
             "title": "One language",
             "body": "Python, TypeScript, C, React and React Native behind one minimal syntax."
         },
         {
             "num": "02",
             "id": "no-glue",
             "title": "No glue",
             "body": "The compiler and runtime generate the APIs, storage and deployment."
         },
         {
             "num": "03",
             "id": "every-platform",
             "title": "Every platform",
             "body": "One codebase projects to web, desktop, mobile, CLI and cloud."
         },
         {
             "num": "04",
             "id": "agents",
             "title": "Agents built in",
             "body": "Objects become agents through walkers and `by llm()`."
         },
         {
             "num": "05",
             "id": "readable",
             "title": "Readable in tiers",
             "body": "Wiring, then contracts, then bodies. Read only as deep as you need."
         },

     ];

def:pub HomeHero -> JsxElement {
    def go(sec_id: str) {
        el: any = document.getElementById(sec_id);
        if el {
            el.scrollIntoView({"behavior": "smooth", "block": "start"});
        }
    }

    return
        <section className="pt-36 pb-20 sm:pt-44 sm:pb-28">
            <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
                <p
                    className="anim-fade-up font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground"
                >
                    The Jac programming language
                </p>
                <h1
                    className="anim-fade-up anim-d1 mt-6 max-w-4xl text-balance text-5xl font-semibold tracking-tight sm:text-6xl lg:text-7xl"
                >
                    The ultimate language for agents to build{" "}
                    <span className="text-primary">everything</span>
                    .
                </h1>
                <p
                    className="anim-fade-up anim-d2 mt-8 max-w-2xl text-pretty text-lg leading-8 text-muted-foreground sm:text-xl sm:leading-9"
                >
                    Jac lets agents write frontend, backend, mobile and native applications in one Pythonic syntax that compiles to Rust-level performance, so a single codebase ships to every platform with ten times less code.
                </p>
                <div
                    className="anim-fade-up anim-d3 mt-10 flex flex-col gap-3 sm:flex-row sm:items-center"
                >
                    <CopyCommand
                        command={HOME_INSTALL}
                        className="w-full sm:w-auto sm:max-w-md"
                    />
                    <Link
                        to="/docs/latest"
                        className={buttonVariants().call(None, {"size": "lg"})}
                    >
                        Get started
                    </Link>
                    <Link
                        to="/tech-demo"
                        className={buttonVariants().call(
                            None, {"variant": "ghost", "size": "lg"}
                        )}
                    >
                        Tech demo →
                    </Link>
                </div>
                <ol
                    className="anim-fade-up anim-d4 mt-20 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-2 lg:mt-28 lg:grid-cols-5"
                >
                    {for p in _PILLARS {
                        <li key={p["id"]}>
                            <button
                                onClick={lambda { go(p["id"]); }}
                                className="group block w-full border-t border-border pt-5 text-left transition-colors hover:border-primary"
                            >
                                <span className="font-mono text-xs text-primary">
                                    {p["num"]}
                                </span>
                                <span
                                    className="mt-2 block text-base font-semibold tracking-tight"
                                >
                                    {p["title"]}
                                </span>
                                <span
                                    className="mt-2 block text-sm leading-relaxed text-muted-foreground"
                                >
                                    <Prose text={p["body"]}/>
                                </span>
                            </button>
                        </li>
                    }}
                </ol>
            </div>
        </section>;
}
