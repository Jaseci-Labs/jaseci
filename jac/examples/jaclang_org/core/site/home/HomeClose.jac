import from "@jac/runtime" { Link }

glob _INSTALL: str = "curl -fsSL https://jaclang.org/install.sh | bash",
     _NEXT: list[dict[str, str]] = [
         {
             "to": "/tech-demo",
             "title": "Tech demo",
             "body": "The full tour: a WebAssembly game, the live source of this site, the mobile app, the polypiler and gradual borrow checking."
         },
         {
             "to": "/docs/latest",
             "title": "Documentation",
             "body": "Install the binary, build a first app, and read the language reference."
         },
         {
             "to": "/wait-wuuut",
             "title": "Wait, Wuuut?!",
             "body": "The ideas behind Jac, from synechic design to topokinetic computation."
         },

     ];

def:pub HomeClose -> JsxElement {
    return
        <HomeSection id="start">
            <Reveal>
                <div className="max-w-3xl">
                    <h2
                        className="text-balance text-4xl font-semibold tracking-tight sm:text-5xl"
                    >
                        Give your agent one language.
                    </h2>
                    <p
                        className="mt-6 max-w-2xl text-pretty text-lg leading-8 text-muted-foreground"
                    >
                        <Prose
                            text="One install, then point any coding agent at the binary. A first prompt that works: build me an app in Jac, the `jac` binary is installed and documents itself with `jac guide`."
                        />
                    </p>
                    <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                        <CopyCommand
                            command={_INSTALL}
                            className="w-full sm:w-auto sm:max-w-md"
                        />
                        <CopyCommand
                            command="claude mcp add jac -- jac mcp"
                            className="w-full sm:w-auto sm:max-w-sm"
                        />
                    </div>
                </div>
            </Reveal>
            <Reveal delay={120}>
                <div className="mt-20 grid grid-cols-1 gap-6 sm:grid-cols-3">
                    {for n in _NEXT {
                        <Link
                            key={n["to"]}
                            to={n["to"]}
                            className="group block border-t border-border pt-5 transition-colors hover:border-primary"
                        >
                            <span
                                className="flex items-center justify-between text-lg font-semibold tracking-tight"
                            >
                                {n["title"]}
                                <span
                                    className="text-muted-foreground transition-transform group-hover:translate-x-1 group-hover:text-primary"
                                >
                                    →
                                </span>
                            </span>
                            <span
                                className="mt-2 block text-sm leading-relaxed text-muted-foreground"
                            >
                                {n["body"]}
                            </span>
                        </Link>
                    }}
                </div>
            </Reveal>
        </HomeSection>;
}
