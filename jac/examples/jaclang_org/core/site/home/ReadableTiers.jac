glob _ARCH_LINES: list[str] = [
         "graph import {",
         "    edge AppOverCore: core.* --> cli.* | desktop.* | mobile.* | web.*;",
         "    edge CoreInternal: core.* --> core.*;",
         "",
         "    core.install ++> web.main;",
         "    core.site.home.Home ++> desktop.pages.index | web.pages.index { Home }",
         "    core.social_graph ++> cli.commands.feed { create_tweet, load_feed }",
         "}",

     ],
     _DECL_LINES: list[str] = [
         "obj RepoMeta {",
         "    has full_name: str = \"\",",
         "        default_branch: str = \"main\",",
         "        stars: int = 0;",
         "}",
         "",
         "def headers(agent: str, accept_json: bool = True) -> dict[str, str];",
         "",
         "def:protect repo_meta(repo: str, agent: str) -> RepoMeta | None;",
         "",
         "def:protect head_sha(repo: str, ref: str, agent: str) -> str;",

     ],
     _IMPL_LINES: list[str] = [
         "impl headers(agent: str, accept_json: bool = True) -> dict[str, str] {",
         "    h: dict[str, str] = {\"User-Agent\": agent};",
         "    if accept_json {",
         "        h[\"Accept\"] = \"application/vnd.github+json\";",
         "    }",
         "    tok = os.environ.get(\"GITHUB_TOKEN\", \"\");",
         "    if tok {",
         "        h[\"Authorization\"] = \"Bearer \" + tok;",
         "    }",
         "    return h;",
         "}",

     ],
     _SCOPES: list[dict[str, str]] = [
         {
             "tier": "1",
             "name": "Wiring",
             "scope": "the whole project: every module and every edge",
             "width": "100%"
         },
         {
             "tier": "2",
             "name": "Declarations",
             "scope": "one module: its types and signatures",
             "width": "62%"
         },
         {
             "tier": "3",
             "name": "Implementations",
             "scope": "one function: its body",
             "width": "30%"
         },

     ];

def:pub ScopeBars -> JsxElement {
    return
        <div className="flex flex-col gap-3">
            {for s in _SCOPES {
                <div
                    key={s["tier"]}
                    className="flex flex-col gap-1.5 sm:flex-row sm:items-center sm:gap-4"
                >
                    <span
                        className="w-52 shrink-0 font-mono text-xs text-muted-foreground"
                    >
                        <span className="text-primary">{"tier " + s["tier"]}</span>
                        {" · " + s["name"]}
                    </span>
                    <div className="min-w-0 flex-1">
                        <div
                            className="flex h-9 items-center rounded-md border border-primary/40 bg-primary/[0.08] px-3"
                            style={{"width": s["width"], "minWidth": "max-content"}}
                        >
                            <span className="truncate text-xs text-foreground">
                                {s["scope"]}
                            </span>
                        </div>
                    </div>
                </div>
            }}
        </div>;
}

def:pub CheckLink(text: str) -> JsxElement {
    return
        <div className="relative flex gap-4 py-6 pl-[19px]">
            <span className="w-px shrink-0 bg-border"></span>
            <p className="max-w-2xl pl-5 text-sm leading-relaxed text-muted-foreground">
                <span
                    className="mr-2 font-mono text-xs uppercase tracking-widest text-primary"
                >
                    checked
                </span>
                <Prose text={text}/>
            </p>
        </div>;
}

def:pub TierRow(
    tier: str, name: str, question: str, file: str, when: str, lines: list[str]
) -> JsxElement {
    return
        <div
            className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)] lg:gap-10"
        >
            <div className="flex gap-5">
                <span
                    className="flex size-10 shrink-0 items-center justify-center rounded-full border border-primary/60 font-mono text-sm text-primary"
                >
                    {tier}
                </span>
                <div className="min-w-0">
                    <h3 className="text-xl font-semibold tracking-tight">{name}</h3>
                    <p className="mt-1 text-base text-foreground/90">{question}</p>
                    <p className="mt-3 font-mono text-xs text-muted-foreground">
                        {file}
                    </p>
                    <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                        <Prose text={when}/>
                    </p>
                </div>
            </div>
            <CodeWindow lines={lines} title={file} className="self-start"/>
        </div>;
}

def:pub ReadableTiers -> JsxElement {
    return
        <HomeSection id="readable">
            <SectionHead
                num="05"
                kicker="Readable in tiers"
                title="Readable and verifiable, one tier at a time."
                lede="Nobody should have to read everything to change anything. A Jac project reads top down in three tiers: `archwire.jac` is the whole architecture, declaration modules are each module's contract, and implementation files hold the bodies. An agent or a reviewer stops at the first tier that answers the question."
            />
            <Figure
                label="fig. 6"
                caption="Each tier describes less of the system in more detail. Most questions about a codebase are answered by the first two."
            >
                <ScopeBars/>
            </Figure>
            <Figure
                label="fig. 7"
                caption="The three tiers, quoted from the repository that serves this page: its wiring, the GitHub client's declarations in `core/github.jac`, and one body from `core/impl/github.impl.jac`."
            >
                <div className="flex flex-col">
                    <TierRow
                        tier="1"
                        name="Wiring"
                        question="Which modules feed which?"
                        file="archwire.jac"
                        when="Rules bound what may depend on what, and each wire is an import with its consumer attached. Modules never write imports of each other; the compiler weaves them in from here."
                        lines={_ARCH_LINES}
                    />
                    <CheckLink
                        text="An import between modules that `archwire.jac` does not declare is a compile error, and so is a wired name that nobody reads. The map cannot drift from the code."
                    />
                    <TierRow
                        tier="2"
                        name="Declarations"
                        question="What does this module promise?"
                        file="core/github.jac"
                        when="Types and signatures with no bodies. It reads like an API reference because it is one, and it is small enough to drop into an agent's context whole."
                        lines={_DECL_LINES}
                    />
                    <CheckLink
                        text="Every caller is type-checked against these signatures, so a body can change without anyone re-reading the code that calls it."
                    />
                    <TierRow
                        tier="3"
                        name="Implementations"
                        question="How does it actually work?"
                        file="core/impl/github.impl.jac"
                        when="The bodies, at the lowest tier. Open one only to change behaviour; large modules split them by concern across several impl files."
                        lines={_IMPL_LINES}
                    />
                </div>
            </Figure>
            <Reveal delay={150}>
                <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
                    <Fact
                        title="Agents read less"
                        body="Finding where something lives takes tier 1. Using a module takes tier 2. Only a change to behaviour opens tier 3."
                    />
                    <Fact
                        title="Architecture shows up in review"
                        body="A new dependency is a one-line change to `archwire.jac`, visible in the diff instead of buried at the top of some file."
                    />
                    <Fact
                        title="The diagram is the system"
                        body="`jac arch graph` renders the wiring as a diagram, and because the wiring generates the imports, that diagram is always current."
                    />
                </div>
            </Reveal>
        </HomeSection>;
}
