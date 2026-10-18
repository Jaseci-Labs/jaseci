impl random_guide(previous: str) -> GuideSample | None {
    try {
        import from jaclang.cli.guide_store { list_docs, guide_sections }
        docs = list_docs();
        choices = [
            g
            for g in docs
            if g.name != previous
        ];
        if not choices {
            return None;
        }
        random.shuffle(choices);
        for guide in choices {
            sections = [
                s
                for s in guide_sections(guide)
                if len(s.body.strip()) > 80
            ];
            if not sections {
                continue;
            }
            section = random.choice(sections);
            return GuideSample(
                title=guide.name,
                body=section.body[:2400],
                url="https://jaclang.org/docs/latest/" + guide.name
            );
        }
        return None;
    } except Exception {
        return None;
    }
}

impl optional_fact(sample: GuideSample) -> str {
    try {
        fact = write_fact(sample.title, sample.body).text.strip();
        if not fact or len(fact) > 160 {
            return "";
        }
        content = fact + "\n" + sample.url;
        return content if len(content) <= 280 else "";
    } except Exception {
        return "";
    }
}
