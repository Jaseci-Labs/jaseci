import from "motion/react" { motion }

glob ConvPath: any = motion.path,
     _STACKS: list[dict[str, str]] = [
         {
             "name": "Python",
             "eco": "PyPI · servers, data, ML",
             "tools": "pyproject.toml · pip · venv"
         },
         {
             "name": "TypeScript",
             "eco": "npm · browser logic",
             "tools": "package.json · tsc · node"
         },
         {
             "name": "C / C++ / Rust",
             "eco": "C ABI · systems, speed",
             "tools": "CMakeLists.txt · Cargo.toml"
         },
         {"name": "React", "eco": "web UI", "tools": "vite.config.ts · JSX"},
         {
             "name": "React Native",
             "eco": "iOS and Android UI",
             "tools": "metro.config.js · app.json"
         },

     ],
     _TARGETS: list[dict[str, str]] = [
         {"name": "Python bytecode", "sub": "server · every PyPI package"},
         {"name": "JavaScript", "sub": "browser + React Native · npm"},
         {"name": "Native code · wasm", "sub": "LLVM · any C-ABI library"},

     ],
     _IMPORTS: list[dict[str, str]] = [
         {
             "code": "import from sklearn.linear_model { LinearRegression }",
             "eco": "PyPI",
             "out": "Python bytecode, on the server"
         },
         {
             "code": "import from \"date-fns\" { format }",
             "eco": "npm",
             "out": "JavaScript, in the browser"
         },
         {
             "code": "import from \"libm.so\" { def sqrt(x: f64) -> f64; }",
             "eco": "C ABI",
             "out": "native machine code"
         },

     ];

def:pub ConvergeDiagram -> JsxElement {
    return
        <div className="overflow-x-auto">
            <svg
                viewBox="0 0 1000 470"
                className="w-full min-w-[760px]"
                role="img"
                aria-label="Python, TypeScript, C, C++ and Rust, React and React Native, each with its own toolchain, converge into Jac, one language that compiles to Python bytecode, JavaScript and native code"
            >
                <text
                    x="0"
                    y="16"
                    fontSize="11"
                    fontFamily="monospace"
                    letterSpacing="2"
                    fill="var(--muted-foreground)"
                >
                    TODAY · FIVE STACKS, FIVE TOOLCHAINS
                </text>
                <text
                    x="1000"
                    y="16"
                    textAnchor="end"
                    fontSize="11"
                    fontFamily="monospace"
                    letterSpacing="2"
                    fill="var(--muted-foreground)"
                >
                    JAC · ONE PROGRAM, THREE TARGETS
                </text>
                {for (i, s) in enumerate(_STACKS) {
                    <g key={"s" + str(i)}>
                        <rect
                            x="0"
                            y={40 + i * 80}
                            width="300"
                            height="64"
                            rx="10"
                            fill="var(--card)"
                            stroke="var(--border)"
                        />
                        <text
                            x="18"
                            y={40 + i * 80 + 25}
                            fontSize="15"
                            fontWeight="600"
                            fill="var(--foreground)"
                        >
                            {s["name"]}
                        </text>
                        <text
                            x="282"
                            y={40 + i * 80 + 25}
                            textAnchor="end"
                            fontSize="11"
                            fill="var(--muted-foreground)"
                        >
                            {s["eco"]}
                        </text>
                        <text
                            x="18"
                            y={40 + i * 80 + 47}
                            fontSize="11"
                            fontFamily="monospace"
                            fill="var(--muted-foreground)"
                        >
                            {s["tools"]}
                        </text>
                        <ConvPath
                            d={"M300,"
                                + str(72 + i * 80)
                                + " C410,"
                                + str(72 + i * 80)
                                + " 420,232 499,232"}
                            fill="none"
                            stroke="#ff6b35"
                            strokeOpacity="0.45"
                            strokeWidth="1.4"
                            initial={{"pathLength": 0}}
                            whileInView={{"pathLength": 1}}
                            viewport={{"once": True, "amount": 0.4}}
                            transition={{"duration": 0.9, "delay": 0.1 + i * 0.1}}
                        />
                    </g>
                }}
                <polygon
                    points="560,162 621,197 621,267 560,302 499,267 499,197"
                    fill="#ff6b35"
                    stroke="#ff6b35"
                />
                <text
                    x="560"
                    y="232"
                    textAnchor="middle"
                    fontSize="26"
                    fontWeight="700"
                    fontFamily="monospace"
                    fill="#ffffff"
                >
                    jac
                </text>
                <text
                    x="560"
                    y="252"
                    textAnchor="middle"
                    fontSize="10"
                    fontFamily="monospace"
                    fill="#ffffff"
                    fillOpacity="0.9"
                >
                    one language
                </text>
                <text
                    x="560"
                    y="334"
                    textAnchor="middle"
                    fontSize="12"
                    fill="var(--foreground)"
                >
                    one syntax · one type checker
                </text>
                <text
                    x="560"
                    y="352"
                    textAnchor="middle"
                    fontSize="12"
                    fill="var(--muted-foreground)"
                >
                    one binary that is the compiler,
                </text>
                <text
                    x="560"
                    y="368"
                    textAnchor="middle"
                    fontSize="12"
                    fill="var(--muted-foreground)"
                >
                    runtime and package manager
                </text>
                {for (i, t) in enumerate(_TARGETS) {
                    <g key={"t" + str(i)}>
                        <ConvPath
                            d={"M621,232 C700,232 690,"
                                + str(144 + i * 88)
                                + " 760,"
                                + str(144 + i * 88)}
                            fill="none"
                            stroke="#ff6b35"
                            strokeOpacity="0.45"
                            strokeWidth="1.4"
                            initial={{"pathLength": 0}}
                            whileInView={{"pathLength": 1}}
                            viewport={{"once": True, "amount": 0.4}}
                            transition={{"duration": 0.7, "delay": 0.7 + i * 0.12}}
                        />
                        <rect
                            x="760"
                            y={112 + i * 88}
                            width="240"
                            height="64"
                            rx="10"
                            fill="var(--card)"
                            stroke="#ff6b35"
                            strokeOpacity="0.5"
                        />
                        <text
                            x="778"
                            y={112 + i * 88 + 27}
                            fontSize="15"
                            fontWeight="600"
                            fill="var(--foreground)"
                        >
                            {t["name"]}
                        </text>
                        <text
                            x="778"
                            y={112 + i * 88 + 47}
                            fontSize="11"
                            fontFamily="monospace"
                            fill="var(--muted-foreground)"
                        >
                            {t["sub"]}
                        </text>
                    </g>
                }}
            </svg>
        </div>;
}

def:pub ImportTable -> JsxElement {
    return
        <div className="overflow-hidden rounded-xl border border-border/70">
            <div
                className="hidden grid-cols-[minmax(0,1.6fr)_120px_minmax(0,1fr)] gap-6 border-b border-border/70 bg-muted/30 px-5 py-3 font-mono text-[11px] uppercase tracking-widest text-muted-foreground md:grid"
            >
                <span>You write</span>
                <span>Resolves in</span>
                <span>Compiles to</span>
            </div>
            {for (i, row) in enumerate(_IMPORTS) {
                <div
                    key={str(i)}
                    className="grid grid-cols-1 gap-2 border-b border-border/70 px-5 py-4 last:border-b-0 md:grid-cols-[minmax(0,1.6fr)_120px_minmax(0,1fr)] md:items-center md:gap-6"
                >
                    <code
                        className="overflow-x-auto whitespace-pre font-mono text-[13px] text-foreground"
                    >
                        {row["code"]}
                    </code>
                    <span className="font-mono text-xs text-primary">{row["eco"]}</span>
                    <span className="text-sm text-muted-foreground">{row["out"]}</span>
                </div>
            }}
        </div>;
}

def:pub OneLanguage -> JsxElement {
    return
        <HomeSection id="one-language">
            <SectionHead
                num="01"
                kicker="One language"
                title="Many stacks, one language."
                lede="A modern app is five languages, five package managers, and the code that holds them together. Jac puts the whole polyglot behind one syntax and one type checker, so an agent learns one language and can still reach every ecosystem."
            />
            <Figure
                label="fig. 1"
                caption="Each stack on the left brings its own language, config files and toolchain. In Jac they become one program, which the compiler splits into the three targets those ecosystems actually run on."
            >
                <ConvergeDiagram/>
            </Figure>
            <Figure
                label="fig. 2"
                caption="There is one import statement. Where the code runs decides which ecosystem a name resolves against, so PyPI, npm and C libraries are all available without wrappers or bindings."
            >
                <ImportTable/>
            </Figure>
            <Reveal delay={150}>
                <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
                    <Fact
                        title="One grammar to hold"
                        body="An agent keeps one syntax and one set of idioms in context instead of five, and spends its tokens on the problem."
                    />
                    <Fact
                        title="One type checker"
                        body="A mismatch between server, browser and native code is a compile error the agent sees immediately, not a bug at runtime."
                    />
                    <Fact
                        title="A binary that explains itself"
                        body="`jac guide` prints agent-loadable skills and `jac mcp` serves the full manual, offline, from the same binary."
                    />
                </div>
            </Reveal>
        </HomeSection>;
}
