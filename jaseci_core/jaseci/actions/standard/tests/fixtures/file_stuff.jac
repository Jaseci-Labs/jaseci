walker pack_it {
    file.dump_json("data.json", {"hello": 5});
    report file.load_json("data.json");
    file.delete("data.json");
}

global gif = "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII=";

walker bin_load_save {
    file.dump_from_b64("file.gif", global.gif);
    s=file.load_to_b64("file.gif");
    report s;
    file.delete("file.gif");
}


walker kwargs_bin_load_save {
    file.dump_from_b64(b64=global.gif, fn="file.gif");
    s=file.load_to_b64(fn="file.gif");
    report s;
    file.delete(fn="file.gif");
}