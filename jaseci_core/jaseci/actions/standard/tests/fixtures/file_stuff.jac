walker pack_it {
    file.dump_json("data.json", {"hello": 5});
    report file.load_json("data.json");
    file.delete("data.json");
}