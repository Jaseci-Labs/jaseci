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
