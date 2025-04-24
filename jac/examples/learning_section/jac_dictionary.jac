#Introduction
with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    print(car["brand"]);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964, "year": 2020};
    print(car["brand"]);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    print(len(car));
}

#Access Dictionary Items

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    print(car["brand"]);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    print(car.get("brand"));
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    x = car.keys();
    print(x);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    x = car.values();
    print(x);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    x = car.items();
    print(x);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    if "model" in car {
        print(
            "Yes,'model' is one of the keys in the car dictionary."
        );
    }
}

#Change Dictionary Items

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car["year"] = 2018;
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.update({"year": 2020});
    print(car);
}

#Add Items

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car["year"] = 2018;
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.update({"year": 2020});
    print(car);
}

#Remove Items

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.pop("model");
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.popitem();
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    del car["model"];
    print(car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    car.clear();
    print(car);
}

#Loop Dictionaries

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    for x in car {
        print(x);
    }
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    for x in car {
        print(car[x]);
    }
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    for x in car.values() {
        print(x);
    }
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    for x in car.keys() {
        print(x);
    }
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    for (x, y) in car.items() {
        print(x, y);
    }
}

#copy Dictionaries

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    new_car = car.copy();
    print(new_car);
}

with entry {
    car = {"brand": "Ford", "model": "Mustang", "year": 1964};
    new_car = dict(car);
    print(new_car);
}

#Nested Dictionaries

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
