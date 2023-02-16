import {*} with './build_graph_1.jac';

#generate similary score for two blocks of sentences;
walker find_similar_sentences{

    can use.encode;
    can vector.cosine_sim;

    has dialogue_1;
    has dialogue_2;
    has sim_value;

    phrase_1 = "";
    for lot in dialogue_1:
        phrase_1 = phrase_1 + ' ' + lot;

    phrase_2 = "";
    for lot in dialogue_2:
        phrase_2 = phrase_2 + ' ' + lot;

    encode1 = use.encode(phrase_1);
    encode2 = use.encode(phrase_2);

    sim_value =  vector.cosine_sim(encode1,encode2);

}