glob _FPS_MAX: int = 3500,
     _FPS_TICKS: list[dict[str, any]] = [
         {"v": 0, "label": "0"},
         {"v": 1000, "label": "1K"},
         {"v": 2000, "label": "2K"},
         {"v": 3000, "label": "3K"},

     ],
     _RUNS: list[dict[str, any]] = [
         {
             "lang": "Jac",
             "build": "jac build --native",
             "fps": 3225.9,
             "shown": "3,225.9",
             "frames": "25,808",
             "hot": True
         },
         {
             "lang": "Zig",
             "build": "zig build-exe",
             "fps": 3235.7,
             "shown": "3,235.7",
             "frames": "25,886",
             "hot": False
         },
         {
             "lang": "Rust",
             "build": "rustc -C opt-level=3",
             "fps": 3223.1,
             "shown": "3,223.1",
             "frames": "25,785",
             "hot": False
         },
         {
             "lang": "Python",
             "build": "CPython 3.14.6 · ctypes",
             "fps": 1588.4,
             "shown": "1,588.4",
             "frames": "12,708",
             "hot": False
         },

     ],
     _MODES: list[dict[str, str]] = [
         {
             "mode": "none",
             "what": "enforced ownership, no collector, zero reference counting",
             "fps": "149,894",
             "ns": "6,671",
             "digest": "502241830"
         },
         {
             "mode": "rc",
             "what": "reference counting",
             "fps": "151,681",
             "ns": "6,593",
             "digest": "502241830"
         },
         {
             "mode": "cycles",
             "what": "reference counting + cycle collector",
             "fps": "137,694",
             "ns": "7,262",
             "digest": "502241830"
         },

     ];

def fps_pct(v: float) -> str;

impl fps_pct(v: float) -> str {
    return str(v * 100 / _FPS_MAX) + "%";
}

def:pub FpsBars -> JsxElement {
    has hover: int = -1;

    return
        <div className="min-w-0">
            <div className="relative">
                {for t in _FPS_TICKS {
                    <span
                        key={t["label"]}
                        className="absolute top-0 bottom-6 w-px bg-border/70"
                        style={{"left": fps_pct(t["v"])}}
                    ></span>
                }}
                <div className="relative flex flex-col gap-7 pt-1 pb-8">
                    {for (i, r) in enumerate(_RUNS) {
                        <div
                            key={r["lang"]}
                            className="relative"
                            onMouseEnter={lambda { hover = i; }}
                            onMouseLeave={lambda { hover = -1; }}
                        >
                            <p className="mb-2 flex items-baseline gap-2 text-sm">
                                <span className="font-medium text-foreground">
                                    {r["lang"]}
                                </span>
                                <span
                                    className="font-mono text-[11px] text-muted-foreground"
                                >
                                    {r["build"]}
                                </span>
                            </p>
                            <div className="flex h-6 items-center gap-3">
                                <div
                                    className="h-6 rounded-r-[4px] transition-opacity"
                                    style={{
                                        "width": fps_pct(r["fps"]),
                                        "backgroundColor": "#ff6b35"
                                            if r["hot"]
                                            else "var(--muted-foreground)",
                                        "opacity": "1"
                                            if (hover == -1 or hover == i)
                                            else "0.45"
                                    }}
                                ></div>
                                <span
                                    className="shrink-0 text-sm font-semibold tabular-nums text-foreground"
                                >
                                    {r["shown"]}
                                </span>
                            </div>
                            {if hover == i {
                                <div
                                    role="tooltip"
                                    className="absolute top-full left-0 z-10 mt-2 rounded-md border border-border bg-popover px-3 py-2 text-xs text-popover-foreground shadow-md"
                                >
                                    <span className="font-semibold tabular-nums">
                                        {r["shown"]} FPS
                                    </span>{" "}
                                    {"average, " + r["frames"] + " frames in 8 s"}
                                </div>
                            }}
                        </div>
                    }}
                </div>
                <div className="relative h-5">
                    {for t in _FPS_TICKS {
                        <span
                            key={t["label"]}
                            className="absolute -translate-x-1/2 font-mono text-[10px] tabular-nums text-muted-foreground"
                            style={{"left": fps_pct(t["v"])}}
                        >
                            {t["label"]}
                        </span>
                    }}
                </div>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">
                average frames per second, uncapped
            </p>
            <table className="sr-only">
                <caption>Average FPS of the raylib cube shooter, by language</caption>
                <thead>
                    <tr>
                        <th>Language</th>
                        <th>Average FPS</th>
                        <th>Frames in 8 seconds</th>
                    </tr>
                </thead>
                <tbody>
                    {for r in _RUNS {
                        <tr key={r["lang"]}>
                            <td>{r["lang"]}</td>
                            <td>{r["shown"]}</td>
                            <td>{r["frames"]}</td>
                        </tr>
                    }}
                </tbody>
            </table>
        </div>;
}

def:pub ModeTable -> JsxElement {
    return
        <div className="overflow-x-auto rounded-xl border border-border/70">
            <table className="w-full min-w-[560px] text-left text-sm">
                <thead
                    className="border-b border-border/70 bg-muted/30 font-mono text-[11px] uppercase tracking-widest text-muted-foreground"
                >
                    <tr>
                        <th className="px-5 py-3 font-normal">Memory mode</th>
                        <th className="px-5 py-3 text-right font-normal">Sim FPS</th>
                        <th className="px-5 py-3 text-right font-normal">ns / frame</th>
                        <th className="px-5 py-3 text-right font-normal">
                            Output digest
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {for m in _MODES {
                        <tr
                            key={m["mode"]}
                            className="border-b border-border/70 last:border-b-0"
                        >
                            <td className="px-5 py-3">
                                <span className="font-mono text-foreground">
                                    {m["mode"]}
                                </span>
                                <span className="ml-2 text-xs text-muted-foreground">
                                    {m["what"]}
                                </span>
                            </td>
                            <td className="px-5 py-3 text-right tabular-nums">
                                {m["fps"]}
                            </td>
                            <td
                                className="px-5 py-3 text-right tabular-nums text-muted-foreground"
                            >
                                {m["ns"]}
                            </td>
                            <td
                                className="px-5 py-3 text-right font-mono text-xs tabular-nums"
                            >
                                {m["digest"]}
                            </td>
                        </tr>
                    }}
                </tbody>
            </table>
        </div>;
}

def:pub NativeBench -> JsxElement {
    return
        <HomeSection id="benchmark">
            <SectionHead
                num=""
                kicker="Benchmark"
                title="Rust-level performance, measured."
                lede="The raylib cube shooter is written four times, line for line, in Jac, Zig, Rust and Python. All four call the same precompiled raylib and do identical work every frame. The Jac build, compiled by `jac build --native` with no C compiler or system linker, renders as fast as Zig and Rust and twice as fast as Python."
            />
            <Figure
                label="fig. 4"
                caption="Average frame rate of each build over an 8-second uncapped run on an Apple M5 Max (macOS 26.5), measured by the example's own `./demo.sh` protocol. Python is CPython 3.14.6 calling the same raylib through `ctypes`, averaged over three runs. A single run moves by a few percent; across repeated runs Jac, Zig and Rust stay within about 3% of each other and their order changes."
            >
                <div
                    className="grid grid-cols-1 items-center gap-10 lg:grid-cols-[minmax(0,260px)_minmax(0,1fr)] lg:gap-14"
                >
                    <div>
                        <p
                            className="text-6xl font-semibold tracking-tight text-foreground sm:text-7xl"
                        >
                            0.4%
                        </p>
                        <p className="mt-2 text-base font-medium">
                            between Jac, Zig and Rust
                        </p>
                        <p
                            className="mt-4 text-sm leading-relaxed text-muted-foreground"
                        >
                            Jac averaged 3,225.9 FPS, between Zig at 3,235.7 and Rust at 3,223.1, and 2× the 1,588.4 of the same game in Python.
                        </p>
                    </div>
                    <FpsBars/>
                </div>
            </Figure>
            <Figure
                label="fig. 5"
                caption="The same game loop without a window, built from one unchanged source under each of Jac's memory modes and run for 100,000 frames. The fully borrow-checked build, with no collector and no reference counting, keeps pace with reference counting, and all three produce the identical output digest."
            >
                <ModeTable/>
            </Figure>
            <Reveal delay={150}>
                <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
                    <Fact
                        title="No C toolchain"
                        body="`jac build --native` emits the object code and writes the executable itself, so there is no `cc` or `ld` in the build."
                    />
                    <Fact
                        title="Same library, same work"
                        body="Each twin binds raylib's C API directly, with no headers or bindings crate, and draws through the same `rlgl` calls."
                    />
                    <Fact
                        title="Run it yourself"
                        body="`./demo.sh` in `jac/examples/raylib_shooter` builds the Jac, Zig and Rust twins and prints this table, and `python3 shooter.py` runs the Python one."
                    />
                </div>
            </Reveal>
        </HomeSection>;
}
