import:py from mtllm.llms, OpenAI;

glob llm = OpenAI();

obj Essay {
    has essay: str;

    can 'Evaluate the given essay based on the given criteria. Provide Detailed Judgement.'
    essay_judge(criteria: str) -> str by llm(incl_info=(self.essay));
    can generate_summary(judgements: dict) -> str by llm(incl_info=(self.essay));
    can give_grade(summary: str) -> 'A to D': str by llm();
}

with entry{
    essay = "With a population of approximately 45 million Spaniards and 3.5 million immigrants,"
            "Spain is a country of contrasts where the richness of its culture blends it up with"
            "the variety of languages and dialects used. Being one of the largest economies worldwide,"
            "and the second largest country in Europe, Spain is a very appealing destination for tourists"
            "as well as for immigrants from around the globe. Almost all Spaniards are used to speaking at"
            "least two different languages, but protecting and preserving that right has not been"
            "easy for them.Spaniards have had to struggle with war, ignorance, criticism and the governments,"
            "in order to preserve and defend what identifies them, and deal with the consequences.";
    essay = Essay(essay);

    criterias = ["Clarity", "Originality", "Evidence"];
    judgements = {};
    for criteria in criterias {
        judgement = essay.essay_judge(criteria);
        judgements[criteria] = judgement;
    }
    summary = essay.generate_summary(judgements);
    grade = essay.give_grade(summary);
    print("Reviewer Notes: ", summary);
    print("Grade: ", grade);
}