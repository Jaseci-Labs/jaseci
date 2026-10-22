impl RubricTable(cols: list[str], rows: list[list[str]]) -> JsxElement {
    return
        <table className="mt-3 w-full border-collapse text-sm">
            <thead>
                <tr className="border-b border-border/70">
                    <th
                        className="pb-2 text-left font-mono text-[10px] uppercase tracking-widest text-muted-foreground"
                    >
                        {cols[0]}
                    </th>
                    <th
                        className="w-16 pb-2 text-right font-mono text-[10px] uppercase tracking-widest text-muted-foreground"
                    >
                        {cols[1]}
                    </th>
                    <th
                        className="hidden pb-2 pl-4 text-left font-mono text-[10px] uppercase tracking-widest text-muted-foreground sm:table-cell"
                    >
                        {cols[2]}
                    </th>
                </tr>
            </thead>
            <tbody>
                {for row in rows {
                    <tr key={row[0]} className="border-b border-border/40">
                        <td className="pt-2.5 pb-2.5 pr-3 align-top font-medium">
                            {row[0]}
                        </td>
                        <td
                            className="pt-2.5 pb-2.5 text-right align-top font-mono tabular-nums text-primary"
                        >
                            {row[1]}
                        </td>
                        <td
                            className="hidden pt-2.5 pb-2.5 pl-4 align-top text-[13px] leading-5 text-muted-foreground sm:table-cell"
                        >
                            {row[2]}
                        </td>
                    </tr>
                }}
            </tbody>
        </table>;
}

impl Section(title: str, total: str, blurb: str) -> JsxElement {
    return
        <div className="mt-10 flex items-baseline gap-3">
            <h2 className="text-xl font-semibold">{title}</h2>
            <span className="font-mono text-sm text-primary">{total}</span>
            <span className="hidden text-sm text-muted-foreground sm:inline">
                {blurb}
            </span>
        </div>;
}

impl Methodology -> JsxElement {
    return
        <section className="relative overflow-hidden py-8">
            <div className="hero-glow absolute inset-0"></div>
            <GraphBackdrop/>
            <div className="relative mx-auto max-w-3xl pl-4 pr-4 sm:pl-6 sm:pr-6">
                <Badge variant="outline" className="mb-4">
                    <HugeiconsIcon
                        icon={ChampionIcon}
                        strokeWidth={2}
                        className="size-3.5"
                    />
                    Ninja Scores
                </Badge>
                <h2 className="text-balance text-2xl font-bold tracking-tight">
                    How the{" "}
                    <span className="text-gradient">score</span>{" "}
                    is earned
                </h2>
                <p className="mt-4 text-muted-foreground">
                    Four categories, 100 points. Every repo is downloaded at a pinned commit and statically read — the code is never executed. Substance and breadth measure the Jac itself, craft measures project hygiene, and community is the one place popularity counts — capped at a fifth of the total, so code always outweighs clout.{" "}
                </p>
                <Section
                    title="Substance"
                    total="30 pts"
                    blurb="how much of the repo is really Jac"
                />
                <RubricTable
                    cols={["Signal", "Max", "How it scales"]}
                    rows={SUBSTANCE_ROWS}
                />
                <Section
                    title="Breadth"
                    total="30 pts"
                    blurb="how much of the language it exercises (capped at 30)"
                />
                <RubricTable
                    cols={["Signal", "Pts", "Detected by"]}
                    rows={BREADTH_ROWS}
                />
                <Section
                    title="Craft"
                    total="20 pts"
                    blurb="project hygiene the author controls"
                />
                <RubricTable cols={["Signal", "Pts", "Earned by"]} rows={CRAFT_ROWS}/>
                <Section
                    title="Community"
                    total="20 pts"
                    blurb="the only place popularity counts"
                />
                <RubricTable
                    cols={["Signal", "Max", "How it scales"]}
                    rows={COMMUNITY_ROWS}
                />
                <Section title="Belts" total="" blurb=""/>
                <div className="mt-3 flex flex-wrap items-center gap-2.5">
                    {for (i, step) in enumerate(BELT_STEPS) {
                        <span key={step[0]} className="flex items-center gap-2.5">
                            {if i > 0 {
                                <span
                                    className="font-mono text-xs text-muted-foreground"
                                >
                                    {step[1] + " →"}
                                </span>
                            }}
                            <span
                                className={"rounded-full pl-2.5 pr-2.5 pt-0.5 pb-0.5 text-xs font-semibold "
                                    + belt_class(step[0])}
                            >
                                {belt_label(step[0])}
                            </span>
                        </span>
                    }}
                </div>
                <p
                    className="mt-10 border-t border-border/40 pt-4 text-[13px] leading-6 text-muted-foreground"
                >
                    Fine print: analysis reads the default branch pinned to its head commit, so every score links to the exact tree it measured. Repos rescore at most once every 6 hours. Downloads are capped at 50 MB per repo and only the relevant slice of each archive is extracted. Click any card on the board for its point-by-point breakdown. Scoring itself is its own app: this workspace's jac.toml declares the scorer as a service app rooted at{" "}
                    <code>core/scoring_service.jac</code>
                    , and the site's server consumes it through one plain import — no HTTP client code anywhere. It shares the server's process during development and runs as its own process in the fleet; each card's breakdown names the process that scored it.
                </p>
            </div>
        </section>;
}
