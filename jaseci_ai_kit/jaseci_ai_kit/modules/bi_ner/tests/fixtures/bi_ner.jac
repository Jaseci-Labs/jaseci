walker test_bi_ner_infer{
    can bi_ner.infer;
    report bi_ner.infer(["The peri-kappa B site mediates human immunodeficiency virus type 2 enhancer activation in monocytes but not in T cells"]);
}


walker test_bi_ner_train{
    can bi_ner.train;
    dataset={
            "text": [
                "IL-2 gene expression and NF-kappa B activation through CD28 requires reactive oxygen production by 5-lipoxygenase.",
                "Activation of the CD28 surface receptor provides a major costimulatory signal for T cell activation resulting in enhanced production of interleukin-2 (IL-2) and cell proliferation."
            ],
            "annotations": [
                [
                    {
                        "start_index": 0,
                        "end_index": 9,
                        "entity_type": "G#DNA"
                    },
                    {
                        "start_index": 25,
                        "end_index": 35,
                        "entity_type": "G#protein"
                    },
                    {
                        "start_index": 55,
                        "end_index": 59,
                        "entity_type": "G#protein"
                    },
                    {
                        "start_index": 99,
                        "end_index": 113,
                        "entity_type": "G#protein"
                    }
                ],
                [
                    {
                        "start_index": 18,
                        "end_index": 22,
                        "entity_type": "G#protein"
                    },
                    {
                        "start_index": 18,
                        "end_index": 39,
                        "entity_type": "G#protein"
                    },
                    {
                        "start_index": 136,
                        "end_index": 149,
                        "entity_type": "G#protein"
                    },
                    {
                        "start_index": 151,
                        "end_index": 155,
                        "entity_type": "G#protein"
                    }
                ]
            ]
    };
    report bi_ner.train(dataset,true,{});
}
