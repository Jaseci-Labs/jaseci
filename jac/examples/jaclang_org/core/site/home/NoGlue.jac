glob _TODO_LINES: list[str] = [
         "node Todo {",
         "    has title: str;",
         "}",
         "",
         "def:pub add_todo(title: str) -> Todo {",
         "    todo = Todo(title=title);",
         "    root ++> todo;",
         "    return todo;",
         "}",
         "",
         "def:pub get_todos -> list[Todo] {",
         "    return [root-->][?:Todo];",
         "}",
         "",
         "def:pub todo_app -> JsxElement {",
         "    has todos: list[Todo] = [];",
         "",
         "    async can with entry {",
         "        todos = await get_todos();",
         "    }",
         "",
         "    return <ul>{[<li key={jid(t)}>{t.title}</li> for t in todos]}</ul>;",
         "}",

     ],
     _GLUE: list[dict[str, any]] = [
         {
             "title": "A node is a persistent type",
             "from": 1,
             "to": 3,
             "body": "Anything reachable from root is saved. There is no schema to declare and no migration to write.",
             "replaces": ["schema.sql", "migrations/", "models.py (ORM)"]
         },
         {
             "title": "`def:pub` is an API endpoint",
             "from": 5,
             "to": 13,
             "body": "A public function becomes an HTTP endpoint with typed, validated inputs and an OpenAPI entry.",
             "replaces": ["routes.py", "request validators", "openapi.yaml"]
         },
         {
             "title": "Connecting a node is the write",
             "from": 7,
             "to": 7,
             "body": "`root ++> todo` stores the todo under the calling user's root, so per-user isolation is the shape of the graph.",
             "replaces": ["db session", "INSERT INTO …", "WHERE user_id = ?"]
         },
         {
             "title": "Components compile to React",
             "from": 15,
             "to": 23,
             "body": "The UI sits beside the logic it uses and compiles to a React bundle, with no separate frontend project.",
             "replaces": ["frontend repo", "package.json", "types.ts (duplicated)"]
         },
         {
             "title": "A remote call is a function call",
             "from": 19,
             "to": 19,
             "body": "`await get_todos()` is an RPC. The HTTP request, serialization and shared types are generated on both sides.",
             "replaces": ["api/client.ts", "fetch wrapper", "JSON serializers"]
         },
         {
             "title": "Deployment is a command",
             "from": 0,
             "to": -1,
             "body": "`jac scale deploy` takes the same program to Kubernetes. The container image and its manifests are derived, not written.",
             "replaces": ["Dockerfile", "docker-compose.yml", "k8s/*.yaml"]
         },

     ];

def:pub GlueMap -> JsxElement {
    has active: int = 0;

    cur = _GLUE[active];
    return
        <div
            className="grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)]"
        >
            <div className="min-w-0">
                <p
                    className="mb-3 font-mono text-[11px] uppercase tracking-widest text-muted-foreground"
                >
                    What the agent writes · 23 lines
                </p>
                <CodeWindow
                    lines={_TODO_LINES}
                    title="todo.jac"
                    numbers={True}
                    hl_from={cur["from"] as int}
                    hl_to={cur["to"] as int}
                />
                {if (cur["from"] as int) == 0 {
                    <div
                        className="code-window mt-3 rounded-xl px-5 py-3 font-mono text-[13px]"
                    >
                        <span className="sh-prompt">$ </span>
                        <span className="sh-cmd">jac scale deploy</span>
                    </div>
                }}
            </div>
            <div className="min-w-0">
                <p
                    className="mb-3 font-mono text-[11px] uppercase tracking-widest text-muted-foreground"
                >
                    What the compiler writes instead
                </p>
                <ol className="flex flex-col">
                    {for (i, g) in enumerate(_GLUE) {
                        <li key={str(i)}>
                            <button
                                onClick={lambda { active = i; }}
                                onMouseEnter={lambda { active = i; }}
                                className={cn(
                                    "block w-full border-l-2 py-3 pr-2 pl-4 text-left transition-colors",
                                    "border-primary bg-primary/[0.06]"
                                        if i == active
                                        else "border-border hover:border-primary/50"
                                )}
                            >
                                <span className="flex items-baseline gap-3">
                                    <span className="font-mono text-xs text-primary">
                                        {str(i + 1)}
                                    </span>
                                    <span
                                        className="text-sm font-semibold tracking-tight"
                                    >
                                        <Prose text={g["title"]}/>
                                    </span>
                                </span>
                                {if i == active {
                                    <span className="mt-2 block pl-6">
                                        <span
                                            className="block text-sm leading-relaxed text-muted-foreground"
                                        >
                                            <Prose text={g["body"]}/>
                                        </span>
                                        <span className="mt-3 flex flex-wrap gap-1.5">
                                            {for (j, f) in enumerate(g["replaces"]) {
                                                <span
                                                    key={str(j)}
                                                    className="strike-chip rounded-md border border-border/80 px-2 py-0.5 font-mono text-[11px] text-muted-foreground"
                                                >
                                                    {f}
                                                </span>
                                            }}
                                        </span>
                                    </span>
                                }}
                            </button>
                        </li>
                    }}
                </ol>
            </div>
        </div>;
}

def:pub NoGlue -> JsxElement {
    return
        <HomeSection id="no-glue">
            <SectionHead
                num="02"
                kicker="No glue"
                title="The compiler writes the glue."
                lede="Glue is most of what an agent emits and the part no tool can check: routes, ORM models, migrations, serializers, API clients and deployment files. Jac's compiler and runtime derive all of it from the program, so the agent writes only the logic, and every line it writes is type-checked."
            />
            <Figure
                label="fig. 3"
                caption="A complete full-stack app. Pick a row to see which lines do the work and which hand-written files they replace. The struck-through files do not exist in a Jac project."
            >
                <GlueMap/>
            </Figure>
            <Reveal delay={150}>
                <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
                    <Fact
                        title="Less to write"
                        body="The agent's output is the application, not the scaffolding around it, so a task takes fewer tokens and fewer turns."
                    />
                    <Fact
                        title="Less to get wrong"
                        body="Generated glue cannot drift. Rename a field and every stale use, on the server or in the browser, is a compile error."
                    />
                    <Fact
                        title="A tighter loop"
                        body="`jac run` serves the app and `jac run --dev` hot-reloads it, so the agent sees each change working in seconds."
                    />
                </div>
            </Reveal>
        </HomeSection>;
}
