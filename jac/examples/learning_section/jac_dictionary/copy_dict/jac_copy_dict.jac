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
