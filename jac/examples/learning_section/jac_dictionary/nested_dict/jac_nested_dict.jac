with entry {
    myfamily = {
        "child1": {"name": "Emil", "year": 2004},
        "child2": {"name": "Tobias", "year": 2007},
        "child3": {"name": "Linus", "year": 2011}
    };
    print(myfamily);
}

with entry {
    child1 = {"name": "Emil", "year": 2004};
    child2 = {"name": "Tobias", "year": 2007};
    child3 = {"name": "Linus", "year": 2011};

    myfamily = {"child1": child1, "child2": child2, "child3": child3};
    print(myfamily);
}

with entry {
    myfamily = {
        "child1": {"name": "Emil", "year": 2004},
        "child2": {"name": "Tobias", "year": 2007},
        "child3": {"name": "Linus", "year": 2011}
    };
    print(myfamily["child2"]["name"]);
}
