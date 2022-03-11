---
sidebar_position: 6
---

# Adding an AI component

Let's add an AI component that suggests best post to members based on their primary interest. For this we'll need to do the following:

- Add an `interest` property to the `person` node
- Create a `post` node
- Set up a predefined list of interests a member can have
- Create a walker to spawn posts on the graph
- Create a walker to get the best suggested post

## Extending the person node

`interest` - a string that represents the primary interest. ex: music, sports, etc

The new person node will look like this.

```
node person {
    has name;

    // new property
    has interest;
}
```

## Creating a post node

The post node will represent a member's post and house the text of that post. It'll also have properties to store the computed relevance of each predefined interest, and the top interest of those. We'll also throw in a property to store the name of the person the post belongs to.

This is what that looks like.

```
node post {
    has body; // post text
    has body_emb; // an embedding (or vector) representation of body
    has body_used_for_emb; // the body value used when body_emb was generated (used for caching and updating embedding)

    has who; // name of post owner

    has interest_scores; // a dictionary that maps the name of each interest to its relevance score
    has top_interest; // the name of the best matching interest
    has top_interest_score; // the score of the best matching interest
}
```

## Set up the interest list

For this we'll create a walker that returns a static list of interests.

```
walker get_interests {
    has anchor interests;

    with entry {
        interests = ['Movies', 'Education', 'Food', 'Cars', 'Music'];
    }

    with exit {
        for i in interests {
            report i;
        }
    }
}
```


## Creating a post and inferring interest

This walker is meant to run on a person and is expected to create a post owned by said person. It will also run a subroutine to generate the embeddings and determine the interest that best matches the body text.

The `update_embeddings` walker creates or updates the embedding for the body of a post using the `USE` external AI service. It also calculates the cosine similarity between the post's body and each of the predefined interests using that embedding. These results are then stored in teach created post so we know which interest it matches best.

```
walker publish_post {
    has body;

    person {
        post = spawn here --> node::post(body=body, who=here.name);
        spawn post walker::update_embeddings;

        report post;
    }
}

walker update_embeddings {
    can use.get_embedding;

    post {
        if ((!here.body_emb && here.body) || (here.body && here.body != here.body_used_for_emb)) {
            here.body_emb = use.get_embedding(here.body);
            here.body_emb = here.body_emb[0];
            here.body_used_for_emb = here.body;

            here.interest_scores = {};
            here.top_interest = '';
            here.top_interest_score = 0.0;
            for i in spawn here walker::get_interests {
                score = vector.cosine_sim((use.get_embedding(i))[0], here.body_emb);
                here.interest_scores[i] = score;
                if (score > here.top_interest_score) {
                    here.top_interest = i;
                    here.top_interest_score = score;
                }
            }
        }
    }
}
```

## Finding the best post for an interest

This walker will check the graph for the best post given an interest as its argument. It checks each post to see if the `top_interest` property matches the requested interest and reports the one with the highest matching score.

```
walker get_best_post {
    has anchor best_post;
    has interest;
    can use.get_embedding;

    with entry {
        best_post = false;
    }

    root {
        take --> node::person;
    }

    person {
        take --> node::post;
    }

    post {
        if (here.top_interest && here.top_interest_score) {
            if (best_post) {
                // compare best_post with current node and overwrite if a better match is found
                if (here.top_interest == interest && here.top_interest_score > best_post.top_interest_score) {
                    best_post = here;
                }
            }
            else {
                // best post has not been set yet; set initial value if interest matches
                if (here.top_interest == interest) {
                    best_post = here;
                }
            }
        }
    }

    with exit {
        report best_post;
    }
}
```

## Demo

Here's a demonstration using the Jaseci API wrapper to simulate how the new functionality can be used.

```
from jac_api import JacApi

if __name__ == '__main__':
    japi = JacApi('http://localhost:8888')
    japi.force_authenticate({
        'email': 'apiuser@example.com',
        'password': 'password'
    })

    with open('social.jac') as f:
        code = f.read()

    graph = japi.create_graph()
    sentinel = japi.create_sentinel()
    gph_id = graph['jid']
    snt_id = sentinel['jid']
    jac = japi.set_jac(snt_id, code)

    # CREATE MEMBERS
    member_nodes = []
    names = ['Jake', 'Amy', 'Charles', 'Rosa', 'Gina']
    interests = japi.run('get_interests', snt_id, gph_id)
    print('INTERESTS', interests)
    for index, name in enumerate(names):
        result = japi.run('join', snt_id, gph_id, {'name': name, 'interest': interests[index]})
        member_nodes.append(result[0])

    print('member nodes', len(member_nodes))

    # CREATE POSTS
    post_nodes = []
    posts_text = [
        'I have the voice of an angel',
        'I like watching Die Hard on weekends',
        'I want to study management at USC',
        'I make a mean sour dough bread',
        'I like driving fast',
    ]

    for index, person in enumerate(member_nodes):
        result = japi.run('publish_post', snt_id, person['jid'], {'body': posts_text[index]})
        post_nodes.append(result[0])

    print('post nodes', len(post_nodes))

    # GET POST SUGGESTIONS
    print('')
    for member in member_nodes:
        member_ctx = member['context']
        interest = member_ctx['interest']
        # sug_posts = japi.run('get_suggested_posts', snt_id, gph_id, {'interest': interest})
        best_post = japi.run('get_best_post', snt_id, gph_id, {'interest': interest})[0]['context']
        print(f'Member: {member_ctx["name"]}')
        print(f'Interest: {member_ctx["interest"]}')
        print('Best post suggestion: ')
        print((best_post['body'], best_post['top_interest_score'], best_post['who']))
        # print(f'Suggested Posts: ')
        # for p in sug_posts:
        #     print((p['context']['body'], p['context']['top_interest_score'], p['context']['who']))
        print('')

    # cleanup
    print('')
    print('CLEANUP')
    print(japi.delete_sentinel(snt_id))
    print(japi.delete_graph(gph_id))
```

