impl StatsBand -> JsxElement {
    return
        <section className="border-y border-border/60 bg-card/40">
            <div
                className="mx-auto max-w-7xl pl-4 pr-4 sm:pl-6 sm:pr-6 lg:pl-8 lg:pr-8"
            >
                <Reveal>
                    <div
                        className="grid grid-cols-2 gap-8 pt-12 pb-12 sm:grid-cols-3 lg:grid-cols-5"
                    >
                        {for (i, s) in enumerate(_STATS) {
                            <div key={str(i)} className="text-center">
                                <div
                                    className="text-3xl font-semibold tabular-nums sm:text-4xl"
                                >
                                    <span className="text-gradient">{s["n"]}</span>
                                    <span className="ml-2 text-foreground">
                                        {s["label"]}
                                    </span>
                                </div>
                                <p className="mt-2 text-sm text-muted-foreground">
                                    {s["sub"]}
                                </p>
                            </div>
                        }}
                    </div>
                </Reveal>
            </div>
        </section>;
}
