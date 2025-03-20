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
