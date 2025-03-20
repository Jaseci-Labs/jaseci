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
