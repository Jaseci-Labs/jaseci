---
sidebar_position: 5
---

# Walkers - Walkers - AI

Let us now move on to the walkers that make use of an AI service.

### Walker: get_suggested_parent

`get_suggested_parent` takes in the title of a new workette as a parameter (`new_wkt_name`) and traverses the workettes on the a day node to find the closest matching existing workette or sub-workette based on their title (`name`) and description (`note`).

Things to note:

- It makes use of the `use.get_embedding` action which connects to the USE AI service included with the Jaseci stack.
- Similarity is determined using the `vector.cosine_sim` global action where the new `name` argument is compared to the `name` and `note` of open top-level workettes as well as the combined embedding of each workette's respective sub-workettes. The final similarity score is determined by the average of these scores.
- Workettes that don't have sub-workettes or ones that do not represent a category / group (`workset`) are skipped, and hence, not suggested.
- It keeps a running note of the best match, which is returned at the end of execution.

```
walker get_suggested_parent {
    has new_wkt_name, new_wkt_name_emb;
    has cur_best_match, cur_best_score;
    can use.get_embedding;

    with entry {
        cur_best_score = 0.0;
        new_wkt_name_emb = use.get_embedding(new_wkt_name);
        new_wkt_name_emb = new_wkt_name_emb[0];
    }

    day {
        take --> node::workette;
    }

    workette {
        if (here.name == new_wkt_name || here.status == 'done' || here.status == 'canceled'): skip;

        has_children = 0;

        spawn here walker::update_embeddings;

        score_count = 0;
        overall_score = 0.0;

        if (here.name_emb) {
            name_sim = vector.cosine_sim(new_wkt_name_emb, here.name_emb);
            overall_score += name_sim * 0.5;
            score_count += 1;
        }
        if (here.note_emb) {
            note_sim = vector.cosine_sim(new_wkt_name_emb, here.note_emb);
            overall_score += note_sim * 0.5;
            score_count += 1;
        }

        for subwkt in -[parent]-> node::workette {
            spawn subwkt walker::update_embeddings;
            subwkt_vec = [];
            if (subwkt.name_emb): subwkt_vec += [subwkt.name_emb];
            if (subwkt.note_emb): subwkt_vec += [subwkt.note_emb];
            if (has_children == 0) {
                children_embeddings = subwkt_vec;
                has_children = 1;
            } else {
                children_embeddings += subwkt_vec;
            }
        }
        if (has_children == 0 && here.wtype != 'workset') {
            skip;
        }

        if (has_children) {
            centroid = vector.get_centroid(children_embeddings);
            centroid_sim = vector.cosine_sim(new_wkt_name_emb, centroid[0]) * centroid[1];
            overall_score += centroid_sim;
            score_count += 1;
        }

        if (score_count > 0): overall_score /= score_count;

        if (overall_score > cur_best_score) {
            cur_best_match = here;
            cur_best_score = overall_score;
        }
        take -[parent]-> node::workette;
    }

    with exit {
        report [cur_best_match, cur_best_score];
    }
}
```

### Walker: update_embeddings

`get_suggested_parent`, when spawned on a workette node, creates a vector representation of its `name` and `note` using the USE AI service. This representation is used in machine learning comparisons, such as `vector.consine_sim`, which determines the similarity between two vectors using a cosine function.

```
walker update_embeddings {
    can use.get_embedding;
    workette {
        # Update embedding via USE if neccessary
        if ((!here.name_emb && here.name) || (here.name && here.name != here.name_used_for_emb)) {
            here.name_emb = use.get_embedding(here.name);
            here.name_emb = here.name_emb[0];
            here.name_used_for_emb = here.name;
        }

        if ((!here.note_emb && here.note) || (here.note && here.note != here.note_used_for_emb)) {
            here.note_emb = use.get_embedding(here.note);
            here.note_emb = here.note_emb[0];
            here.note_used_for_emb = here.note;
        }
    }
}
```
