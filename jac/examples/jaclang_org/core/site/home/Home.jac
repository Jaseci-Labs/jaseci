glob HOME_SECTIONS: list[dict[str, any]] = [
         {"id": "one-language", "label": "one language"},
         {"id": "no-glue", "label": "no glue"},
         {"id": "in-production", "label": "in production"},
         {"id": "benchmark", "label": "benchmark"},
         {"id": "agents", "label": "agents"},
         {"id": "readable", "label": "readable"},
         {"id": "start", "label": "start"},

     ];

def:pub Home -> JsxElement;

impl Home -> JsxElement {
    return
        <>
            <SectionRail items={HOME_SECTIONS}/>
            <HomeHero/>
            <OneLanguage/>
            <NoGlue/>
            <InProduction/>
            <NativeBench/>
            <AgentNative/>
            <ReadableTiers/>
            <HomeClose/>
        </>;
}
