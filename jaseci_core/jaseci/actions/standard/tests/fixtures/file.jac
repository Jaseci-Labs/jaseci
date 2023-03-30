walker new_file {
    can file2.new, file2.open, file2.write, file2.read, file2.close, file2.is_open, file2.to_base64, file2.seek;
    with entry {
        # create file
        uuid = file2.new("testing.text");

        # report current file's uuid
        report uuid;

        # open the current file
        file2.open(uuid, "a+");

        # read current file's content
        report file2.read(uuid);

        # write to the current file
        file2.write(uuid, "0");

        # current pointer will be the end of file and this will print nothing
        report file2.read(uuid);

        # changing the pointer on start of the file
        file2.seek(uuid, 0);

        # will print "0"
        report file2.read(uuid);

        # rewrite again on the current file
        file2.write(uuid, "0");

        # reading file with seeking offset
        # will print "00"
        report file2.read(uuid, offset=0);

        # this will always read the file from the start
        report file2.to_base64(uuid);

        # file is still open
        report file2.is_open(uuid);

        # closing the file
        file2.close(uuid);

        # file is already closed
        report file2.is_open(uuid);
    }
}

walker json_file {
    can file2.new, file2.open, file2.close, file2.attr, file2.dump_json, file2.to_json, file2.detach, file2.delete, file2.exists, file2.load;

    with entry {
        # create empty json
        uuid = file2.new("testing.json");
        file_info = file2.attr(uuid);
        file2.dump_json(uuid, {"testing":1});

        # detaching reference on memory without deleting the file
        file2.detach(uuid, persist = true);

        # read from existing file
        uuid = file2.load(file_info["absolute_path"]);
        report file2.to_json(uuid);
        report file2.exists(uuid);

        # delete the file
        file2.delete(uuid);
        # check if file still exists
        uuid = file2.load(file_info["absolute_path"]);
        report file2.exists(uuid);
    }
}

walker download_file {
    can file2.download, file2.attr;

    with entry {
        uuid = file2.download("https://github.com/Jaseci-Labs/jaseci/raw/main/support/bible/pdf/jaseci_bible.pdf");

        report uuid;
        # return file's attributes
        report file2.attr(uuid);
    }
}

walker return_any_file {
    can file2.download, file2.attr;

    with entry {
        uuid = file2.download("https://github.com/Jaseci-Labs/jaseci/raw/main/support/bible/pdf/jaseci_bible.pdf");

        # return the actual file
        report:file = uuid;
    }
}

walker return_any_file_with_name {
    can file2.download, file2.attr, file2.update;

    with entry {
        uuid = file2.download("https://github.com/Jaseci-Labs/jaseci/raw/main/support/bible/pdf/jaseci_bible.pdf");

        # update the file name and return the actual file
        report:file = file2.update(uuid, name="jaseci_bible.pdf")["id"];
    }
}