# Map the movie data in to a Graph.

The Jasecis one and only data structure used is Graph. So first let's map the movie script in to graph. Movie script is saved in a `json` file, and the basic structure of the movie script is as follows;

```json

{"scene1 name" : ["scene1 description", {"actor1 name": "[actor 1 dialodues]", "actor2 name": "[actor 2 dilogue]"}],

"scene2 name": "scene2 description",
}
```

Sample from the movie script;

```json
{
    "1 EXT. PUENTE ANTIGUO, NEW MEXICO - NIGHT 1": "A main street extends before us in this one-horse town, set amid endless flat, arid scrubland. A large SUV slowly moves down the street and heads out of town.",
    "2 EXT. SUV - NIGHT 2": [
        "The SUV sits parked in the desert. Suddenly, the roof panels of the SUV FOLD OPEN. The underside of the panels house a variety of hand-built ASTRONOMICAL DEVICES, which now point at the sky. JANE FOSTER (late 20's) pops her head through the roof. She positions a MAGNETOMETER, so its monitor calibrates with the constellations above. It appears to be cobbled together from spare parts of other devices.",
        {
            "JANE": [
                "Hurry! We hear a loud BANG followed by muffled CURSING from below. Jane offers a hand down to ERIK SELVIG (60) who emerges as well, rubbing his head. JANE (CONT'D) Oh-- watch your head.",
                "It's a little different each time. Once it looked like, I don't know, melted stars, pooling in a corner of the sky. But last week it was a rolling rainbow ribbon--",
            ],
            "SELVIG": [
                "Thanks. So what's this anomaly of yours supposed to look like?",
                "(GENTLY TEASING) Racing round Orion? I've always said you should have been a poet. Jane reigns in her excitement. She tries for dignity. 4th BLUE REVISIONS 03-26-10 1A.",
                "(re: the gloves) I recognize those. Think how proud he'd be to see you now. Jane's grin fades to a sad smile.",
                "For what?"
            ]
        }
    ],
    "3 INT. SUV - NIGHT 3": [
        "The SUV is bathed in the glow of high-tech monitoring equipment and laptops, some looking like they're held together with duct tape. Jane opens a well-worn NOTEBOOK of handwritten notes and calculations. Selvig watches the frustrated Jane with sympathy.",
        {
            "JANE": [
                "The anomalies are always precipitated by geomagnetic storms. She shows him a complicated CHART she's drawn in the book, tracking occurrences and patterns. I just don't understand. Something catches Darcy's eye out the driver's side mirror. She adjusts it. In the distance",
            ],
            "DARCY": [
                "Jane? Jane SHUSHES her, leafs through her notes. The bottle of champagne begins to vibrate.",
                "The champagne bottle starts to RATTLE noisily now as it shakes more violently, pressure building up inside it, when the cork EXPLODES out of it. Champagne goes spewing everywhere -- over equipment, over Jane. DARCY (CONT'D) Jane?",
            ],
            "SELVIG": [
                "That's your subtle aurora?!"
            ]
        }
    ],
    "4 EXT. DESERT - MOMENTS LATER 4": "The roof panels still open, the SUV races towards the strange event, Jane, amazed by the sight, stands with half her body out the roof, taking video of the light storm before them. The SUV hits a bump. Jane nearly flies out. Selvig grabs her, yanks her back in.",
    "5 INT. SUV 5": [
        "Jane grins, thrilled, pumped with adrenaline.",
        {
            "JANE": [
                "Isn't this great?! A thought strikes her. JANE (CONT'D) You're seeing it too, right? I'm not crazy?"
            ],
            "SELVIG": [
                "That's debateable. Put your seat belt on! 4th BLUE REVISIONS 03-26-10 3A. The SUV lurches."
            ]
        }
    ]
}
```

So, lets dive into the code;

first we will need to have two types of nodes in this graph, `scenes` and `actors` in addition to `root` node.  lets define those nodes in jac.

```jac
node root;

node scene{
    has name;
    has description;
}

node actor{
    has name;
    has dialogue;
}
```

As you can see in the above code the `scene` type nodes has two variable called `name` and `description`. we can define a variable in `jac` with the `has` key word. Similarly the `actor` type nodes has two variable define `name` and `dialogue`. now let's build the graph by connecting these nodes by edges and assigning variables to them.

To build the graph we are creating the build_graph walker. To get more clear picture about Jaseci walkers go to [here](../../CanoniCAI/codelabs/lang_docs/walkers_by_example.md) and [here](../../CanoniCAI/codelabs/lang_docs/walkers.md).

```jac
walker build_graph{

    can file.load_json;

    #loading the movie data to the movie variable.
    has movie = file.load_json("movie_data.json");

    #looping through movie dictionery.
    for movie_scene in movie {
        scene_name = movie_scene;
        content = movie[movie_scene];

        if content.type == str:
            description = content;
            scene = spawn here ++> node::scene(name=scene_name, description=description);

        if content.type == list:
            if content[0].type == str:
                description = content[0];
            scene = spawn here ++> node::scene(name=scene_name, description=description);

            if content[1].type == dict:
                for actor in content[1]{
                    name = actor;
                    dialogue = content[1][actor];
                        spawn scene ++>node::actor(name=name, dialogue=dialogue);
                    }
        }
}
```

In the above block;

- `file.load_json` action is using to load the `json` file. here the name of the `json` file is `movie_data.json`.
- In the line starts with `has movie`, asigns the movie data to the `movie` variable.
- Here the movie data is a dictonery object, contains details of the movie scenes in the each item of the dictionery.
- Jaseci also can supports `for` and `if` syntax similar to the other programming languages, so I'm not going to explain them in deeper.

