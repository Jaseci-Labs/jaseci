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
