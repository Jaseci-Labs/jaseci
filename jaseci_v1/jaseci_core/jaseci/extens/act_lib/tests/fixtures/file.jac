walker new_file {
    can fh.new, fh.open, fh.write, fh.read, fh.close, fh.is_open, fh.to_base64, fh.seek;
    with entry {
        # create file
        uuid = fh.new("testing.text");

        # report current file's uuid
        report uuid;

        # open the current file
        fh.open(uuid, "a+");

        # read current file's content
        report fh.read(uuid);

        # write to the current file
        fh.write(uuid, "0");

        # current pointer will be the end of file and this will print nothing
        report fh.read(uuid);

        # changing the pointer on start of the file
        fh.seek(uuid, 0);

        # will print "0"
        report fh.read(uuid);

        # rewrite again on the current file
        fh.write(uuid, "0");

        # reading file with seeking offset
        # will print "00"
        report fh.read(uuid, offset=0);

        # this will always read the file from the start
        report fh.to_base64(uuid);

        # file is still open
        report fh.is_open(uuid);

        # closing the file
        fh.close(uuid);

        # file is already closed
        report fh.is_open(uuid);
    }
}

walker json_file {
    can fh.new, fh.open, fh.close, fh.attr, fh.dump_json, fh.to_json, fh.detach, fh.delete, fh.exists, fh.load;

    with entry {
        # create empty json
        uuid = fh.new("testing.json");
        file_info = fh.attr(uuid);
        fh.dump_json(uuid, {"testing":1});

        # detaching reference on memory without deleting the file
        fh.detach(uuid, persist = true);

        # read from existing file
        uuid = fh.load(file_info["absolute_path"]);
        report fh.to_json(uuid);
        report fh.exists(uuid);

        # delete the file
        fh.delete(uuid);
        # check if file still exists
        uuid = fh.load(file_info["absolute_path"]);
        report fh.exists(uuid);
    }
}

walker download_file {
    can fh.download, fh.attr;

    with entry {
        uuid = fh.download("https://github.com/Jaseci-Labs/jaseci/raw/main/support/bible/pdf/jaseci_bible.pdf");

        report uuid;
        # return file's attributes
        report fh.attr(uuid);
    }
}

walker return_any_file {
    can fh.download, fh.attr;

    with entry {
        uuid = fh.download("https://github.com/Jaseci-Labs/jaseci/raw/main/support/bible/pdf/jaseci_bible.pdf");

        # return the actual file
        report:file = uuid;
    }
}

walker return_any_file_with_name {
    can fh.download, fh.attr, fh.update;

    with entry {
        uuid = fh.download("https://github.com/Jaseci-Labs/jaseci/raw/main/support/bible/pdf/jaseci_bible.pdf");

        # update the file name and return the actual file
        report:file = fh.update(uuid, name="jaseci_bible.pdf")["id"];
    }
}

walker manual_upload_file {
    can request.multipart, fh.download;

    with entry {
        uuid = fh.download("https://github.com/Jaseci-Labs/jaseci/raw/main/support/bible/pdf/jaseci_bible.pdf");

        request.multipart(
            "https://sample/com",
            data = {
                "test": 1
            },
            files = [uuid],
            header = {
                "test": 2
            }
        );
    }
}