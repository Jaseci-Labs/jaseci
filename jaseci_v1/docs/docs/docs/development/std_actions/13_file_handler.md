# **`File Handler`**
## fh.**`load`**
> **`Arguments`:** \
> **path**: *str*
>
> **`Return`:** \
> file's uuid *(`str`)*
>
> **`Usage`:** \
> loading existing file using local path
>
> **`Remarks`:** \
> content_type will vary on name if not specified
##### **`HOW TO TRIGGER`**
```js
fh.load("test.json");
```
---
## fh.**`new`**
> **`Arguments`:** \
> **name**: str \
> **content_type**: str = None \
> **field**: str = None \
> **persist**: bool = False
>
> **`Return`:** \
> file's uuid *(`str`)*
>
> **`Usage`:** \
> creating file reference (no creation yet)
>
> **`Remarks`:** \
> content_type will vary on name if not specified \
> field is used as request.multipart form field. Default to "`file`" \
> persist is for retaining the file or not after the request is done (or when the Hook is destroyed)
##### **`HOW TO TRIGGER`**
```js
fh.new("test.json");
```
---
## fh.**`update`**
> **`Arguments`:** \
> **id**: str \
> **name**: str = None \
> **content_type**: str = None \
> **field**: str = None \
> **persist**: bool = None
>
> **`Return`:** \
> file's attr *(`dict`)*
>
> **`Usage`:** \
> updating file's reference info
>
> **`Remarks`:** \
> content_type will vary on name if not specified \
> field is used as request.multipart form field. Default to "`file`" \
> persist is for retaining the file or not after the request is done (or when the Hook is destroyed)
##### **`HOW TO TRIGGER`**
```js
fh.update(file_uuid, "test.json", field = "your-custom-field", persist = true);
```
---
## fh.**`read`**
> **`Arguments`:** \
> **id**: str \
> **offset**: int = None
>
> **`Return`:** \
> file's content in string type *(`str`)*
>
> **`Usage`:** \
> reading file's content in string type
>
> **`Remarks`:** \
> offset can be use if you want to have pre `seek(offset)` trigger
##### **`HOW TO TRIGGER`**
```js
fh.read(file_uuid);
```
---
## fh.**`seek`**
> **`Arguments`:** \
> **id**: str \
> **offset**: int \
> **whence**: int = 0
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> change pointer similar to python's seek on opened file
>
> **`Remarks`:** \
> seek will be undone once write is triggered \
> same rules apply from python's seek on opened file
##### **`HOW TO TRIGGER`**
```js
fh.seek(file_uuid, 0);
```
---
## fh.**`open`**
> **`Arguments`:** \
> **id**: str \
> **mode**: str = "r" \
> **encoding**: str = "utf-8" \
> **\*\*kwargs** (additional keyword argument)
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> read the file using mode similar to python's open file
>
> **`Remarks`:** \
> same rules apply from python's open file
##### **`HOW TO TRIGGER`**
```js
fh.open(file_uuid);
```
---
## fh.**`is_open`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> if file is still open *(`bool`)*
>
> **`Usage`:** \
> to check if file is still open
>
> **`Remarks`:** \
> N/A
##### **`HOW TO TRIGGER`**
```js
fh.is_open(file_uuid);
```
---
## fh.**`exists`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> if file is already existing *(`bool`)*
>
> **`Usage`:** \
> to check if file is already existing
>
> **`Remarks`:** \
> N/A
##### **`HOW TO TRIGGER`**
```js
fh.exists(file_uuid);
```
---
## fh.**`write`**
> **`Arguments`:** \
> **id**: str \
> **content**: str
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> to write string content on your file if it's open
>
> **`Remarks`:** \
> currently, we only support writing in string in jac. \
> technically, we `can` still write in bytes but "it's not fully supported yet!"
##### **`HOW TO TRIGGER`**
```js
fh.write(file_uuid, "your custom string");
```
---
## fh.**`flush`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> flush current buffer if it's still open
>
> **`Remarks`:** \
> same rules apply from python's flush on opened file
##### **`HOW TO TRIGGER`**
```js
fh.flush(file_uuid);
```
---
## fh.**`close`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> close the file if it's open
>
> **`Remarks`:** \
> same rules apply from python's flush on opened file
##### **`HOW TO TRIGGER`**
```js
fh.close(file_uuid);
```
---
## fh.**`detach`**
> **`Arguments`:** \
> **id**: str \
> **persist**: bool = None
>
> **`Return`:** \
> file's attr *(`dict`)*
>
> **`Usage`:** \
> close the file and pop the file reference
>
> **`Remarks`:** \
> persist will override current file's persist attribute
##### **`HOW TO TRIGGER`**
```js
fh.detach(file_uuid);
```
---
## fh.**`delete`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> close the file and try to delete it
>
> **`Remarks`:** \
> uses python's os.unlink
##### **`HOW TO TRIGGER`**
```js
fh.delete(file_uuid);
```
---
## fh.**`attr`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:**
> ```js
> {
>    "id": str,
>    "name": str,
>    "content_type": str,
>    "field": str,
>    "absolute_name": str,
>    "absolute_path": str,
>    "persist": bool,
> }
> ```
>
> **`Usage`:** \
> getting file's attributes
>
> **`Remarks`:** \
> N/A
##### **`HOW TO TRIGGER`**
```js
fh.attr(file_uuid);
```
---
## fh.**`to_bytes`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> file's content in bytes *(`bytes`)*
>
> **`Usage`:** \
> reading file content in bytes type
>
> **`Remarks`:** \
> will open the file seperately with mode = "`rb`" and will close after returning the content
##### **`HOW TO TRIGGER`**
```js
fh.to_bytes(file_uuid);
```
---
## fh.**`to_base64`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> file's content in base64 string *(`str`)*
>
> **`Usage`:** \
> reading file content in base64 string type
>
> **`Remarks`:** \
> will open the file seperately with mode = "`rb`" and will close after returning the converted base64 content
##### **`HOW TO TRIGGER`**
```js
fh.to_base64(file_uuid);
```
---
## fh.**`to_json`**
> **`Arguments`:** \
> **id**: str
>
> **`Return`:** \
> file's content in dict type *(`dict`)*
>
> **`Usage`:** \
> reading file content in dictionary type
>
> **`Remarks`:** \
> will open the file seperately with mode = "`r`" and will close after returning the converted json content
##### **`HOW TO TRIGGER`**
```js
fh.to_json(file_uuid);
```
---
## fh.**`dump_json`**
> **`Arguments`:** \
> **id**: str \
> **json**: dict \
> **indent**: int = None
>
> **`Return`:** \
> None
>
> **`Usage`:** \
> writing dictionary obj to the file
>
> **`Remarks`:** \
> similar to write but specifically for json serializable content only
##### **`HOW TO TRIGGER`**
```js
fh.dump_json(file_uuid, {"key": "value"});
```
---
## fh.**`download`**
> **`Arguments`:** \
> **url**: str \
> **header**: dict = {}
>
> **`Return`:** \
> file's uuid *(`str`)*
>
> **`Usage`:** \
> downloading file remotely and creating reference to it
>
> **`Remarks`:** \
> similar to load but this is for remote file
##### **`HOW TO TRIGGER`**
```js
fh.download("https://path/to/file", header={"Authorization":"key"});
```
---

# **`File Report`**
- dev can now report a file
    - `jsserv`: return the actual file
    - `jsctl`: return fh.attr (remote or local)
##### **`HOW TO TRIGGER`**
```js
report:file = uuid;
```
##### **`SAMPLE USAGE`**
```js
walker new_file {
    can fh.load;

    with entry {
        uuid = fh.load("testing.text");

        report:file = uuid;
    }
}
```
---

# **`Sample Codes`**

```python
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
        fh.dump_json(uuid, {"testing":1};

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

walker simple_with_file {
    has sample, fileTypeField;

    with entry {
        report sample;

        if fileTypeField and global.info['request_context']["body"]["ctx"]["fileTypeField"] {
            report true;
        }

        report fileTypeField[0];
        report fh.attr(fileTypeField[0]);
        report fh.read(fileTypeField[0], 0);
        report fh.to_json(fileTypeField[0]);
        report fh.to_bytes(fileTypeField[0]).str;
        report fh.to_base64(fileTypeField[0]);
    }
}

walker simple_custom_payload_with_file {
    has fileTypeField;

    can fh.attr, fh.read, fh.to_json, fh.to_base64, fh.to_bytes;

    with entry {
        if not fileTypeField and not global.info['request_context']["body"]["ctx"] {
            report true;
        }

        uuid = global.info['request_context']["body"]["fileTypeField"][0];
        report uuid;
        report fh.attr(uuid);
        report fh.read(uuid, 0);
        report fh.to_json(uuid);
        report fh.to_bytes(uuid).str;
        report fh.to_base64(uuid);
    }
}


```