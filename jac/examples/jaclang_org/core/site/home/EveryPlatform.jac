import from "motion/react" { motion }

glob FanPath: any = motion.path,
     _TREE: list[dict[str, str]] = [
         {"name": "jac.toml", "note": "declares the apps"},
         {"name": "archwire.jac", "note": "declares the wiring"},
         {"name": "core/", "note": "shared logic, data, UI"},
         {"name": "web/", "note": "entry · pages"},
         {"name": "desktop/", "note": "entry · pages"},
         {"name": "mobile/", "note": "entry"},
         {"name": "cli/", "note": "entry · commands"},

     ],
     _PLATFORMS: list[dict[str, str]] = [
         {
             "name": "Web",
             "runtime": "React in the browser + API server",
             "cmd": "jac run web"
         },
         {
             "name": "Desktop",
             "runtime": "native window over the OS webview",
             "cmd": "jac run desktop"
         },
         {
             "name": "Mobile",
             "runtime": "React Native on iOS and Android",
             "cmd": "jac run mobile"
         },
         {"name": "CLI", "runtime": "a command-line tool", "cmd": "jac run cli"},
         {
             "name": "Cloud services",
             "runtime": "separate processes on Kubernetes",
             "cmd": "jac scale deploy"
         },
         {
             "name": "Native · WebAssembly",
             "runtime": "LLVM machine code, no garbage collector",
             "cmd": "jac build --as native"
         },

     ],
     _TOML_LINES: list[str] = [
         "[apps.web]",
         "kind = \"web-app\"",
         "entry-point = \"web.main\"",
         "",
         "[apps.desktop]",
         "kind = \"desktop\"",
         "entry-point = \"desktop.main\"",
         "",
         "[apps.mobile]",
         "kind = \"mobile\"",
         "entry-point = \"mobile.main\"",
         "",
         "[apps.cli]",
         "kind = \"cli\"",
         "entry-point = \"cli.main\"",
         "",
         "[apps.social_graph]",
         "kind = \"service\"",
         "entry-point = \"core.social_graph\"",

     ];

def:pub ProjectionDiagram -> JsxElement {
    return
        <div className="overflow-x-auto">
            <svg
                viewBox="0 0 1000 470"
                className="w-full min-w-[760px]"
                role="img"
                aria-label="One Jac workspace with a shared core projects to web, desktop, mobile, command line, cloud services and native or WebAssembly builds"
            >
                <text
                    x="0"
                    y="16"
                    fontSize="11"
                    fontFamily="monospace"
                    letterSpacing="2"
                    fill="var(--muted-foreground)"
                >
                    ONE CODEBASE
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
                    SIX PROJECTIONS
                </text>
                <rect
                    x="0"
                    y="40"
                    width="330"
                    height="410"
                    rx="14"
                    fill="var(--card)"
                    stroke="var(--border)"
                />
                <text
                    x="24"
                    y="76"
                    fontSize="14"
                    fontWeight="600"
                    fontFamily="monospace"
                    fill="var(--foreground)"
                >
                    my_app/
                </text>
                {for (i, f) in enumerate(_TREE) {
                    <g key={"f" + str(i)}>
                        <text
                            x="24"
                            y={118 + i * 46}
                            fontSize="13"
                            fontFamily="monospace"
                            fill={"#ff6b35"
                                if f["name"] == "core/"
                                else "var(--foreground)"}
                            fontWeight={"700" if f["name"] == "core/" else "400"}
                        >
                            {("└ " if i == len(_TREE) - 1 else "├ ") + f["name"]}
                        </text>
                        <text
                            x="306"
                            y={118 + i * 46}
                            textAnchor="end"
                            fontSize="11"
                            fill="var(--muted-foreground)"
                        >
                            {f["note"]}
                        </text>
                    </g>
                }}
                <rect
                    x="12"
                    y="188"
                    width="306"
                    height="44"
                    rx="8"
                    fill="#ff6b35"
                    fillOpacity="0.08"
                    stroke="#ff6b35"
                    strokeOpacity="0.4"
                />
                <FanPath
                    d="M318,210 L470,210"
                    fill="none"
                    stroke="#ff6b35"
                    strokeOpacity="0.6"
                    strokeWidth="1.6"
                    initial={{"pathLength": 0}}
                    whileInView={{"pathLength": 1}}
                    viewport={{"once": True, "amount": 0.4}}
                    transition={{"duration": 0.5}}
                />
                <rect
                    x="370"
                    y="195"
                    width="100"
                    height="30"
                    rx="15"
                    fill="var(--background)"
                    stroke="#ff6b35"
                    strokeOpacity="0.6"
                />
                <text
                    x="420"
                    y="215"
                    textAnchor="middle"
                    fontSize="12"
                    fontWeight="700"
                    fontFamily="monospace"
                    fill="#ff6b35"
                >
                    jac
                </text>
                {for (i, p) in enumerate(_PLATFORMS) {
                    <g key={"p" + str(i)}>
                        <FanPath
                            d={"M470,210 C560,210 560,"
                                + str(68 + i * 72)
                                + " 640,"
                                + str(68 + i * 72)}
                            fill="none"
                            stroke="#ff6b35"
                            strokeOpacity="0.45"
                            strokeWidth="1.4"
                            initial={{"pathLength": 0}}
                            whileInView={{"pathLength": 1}}
                            viewport={{"once": True, "amount": 0.4}}
                            transition={{"duration": 0.7, "delay": 0.4 + i * 0.1}}
                        />
                        <rect
                            x="640"
                            y={40 + i * 72}
                            width="360"
                            height="56"
                            rx="10"
                            fill="var(--card)"
                            stroke="var(--border)"
                        />
                        <text
                            x="658"
                            y={40 + i * 72 + 24}
                            fontSize="14"
                            fontWeight="600"
                            fill="var(--foreground)"
                        >
                            {p["name"]}
                        </text>
                        <text
                            x="982"
                            y={40 + i * 72 + 24}
                            textAnchor="end"
                            fontSize="11"
                            fontFamily="monospace"
                            fill="#ff6b35"
                        >
                            {p["cmd"]}
                        </text>
                        <text
                            x="658"
                            y={40 + i * 72 + 43}
                            fontSize="11"
                            fill="var(--muted-foreground)"
                        >
                            {p["runtime"]}
                        </text>
                    </g>
                }}
            </svg>
        </div>;
}

def:pub EveryPlatform -> JsxElement {
    return
        <HomeSection id="every-platform">
            <SectionHead
                num="03"
                kicker="Every platform"
                title="One codebase, every platform."
                lede="An app is a projection of one codebase. A workspace names its apps in `jac.toml`, and the same shared core compiles to a website, a desktop window, a phone app, a command-line tool and cloud services, with one type checker watching all of them at once."
            />
            <Figure
                label="fig. 4"
                caption="Every projection reads the same core. The app directories hold only entry points and pages, and each command builds or runs one projection."
            >
                <ProjectionDiagram/>
            </Figure>
            <Reveal delay={150}>
                <div
                    className="mt-16 grid grid-cols-1 items-start gap-10 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]"
                >
                    <CodeWindow
                        lines={_TOML_LINES}
                        title="jac.toml · the site you are reading"
                        lang="toml"
                    />
                    <div className="grid grid-cols-1 gap-8">
                        <Fact
                            title="This page is the proof"
                            body="jaclang.org is one Jac workspace: the website, the same site as a desktop app, a mobile app, a CLI and two services, all over one shared core directory."
                        />
                        <Fact
                            title="Change once, check everywhere"
                            body="Change a shared type and every app that uses it is re-checked. A break in the mobile app shows up when you edit the core, not after you ship."
                        />
                        <Fact
                            title="Topology is a setting"
                            body="`jac run --serve` colocates the services in one process for development. `--fleet`, and every deploy, gives each its own. The source does not change."
                        />
                    </div>
                </div>
            </Reveal>
        </HomeSection>;
}
