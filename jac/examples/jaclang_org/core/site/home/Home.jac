glob HOME_SECTIONS: list[dict[str, any]] = [
         {"id": "one-language", "label": "one language"},
         {"id": "no-glue", "label": "no glue"},
         {"id": "every-platform", "label": "every platform"},
         {"id": "agents", "label": "agents"},
         {"id": "readable", "label": "readable"},
         {"id": "start", "label": "start"},

     ];

def:pub Home -> JsxElement {
    return
        <>
            <SectionRail items={HOME_SECTIONS}/>
            <HomeHero/>
            <OneLanguage/>
            <NoGlue/>
            <EveryPlatform/>
            <AgentNative/>
            <ReadableTiers/>
            <HomeClose/>
        </>;
}
