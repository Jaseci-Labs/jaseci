# **`File Handler`**
## file2.**`load`**
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
file2.load("test.json");
```
---
## file2.**`new`**
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
file2.new("test.json");
```
---
## file2.**`update`**
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
file2.update(file_uuid, "test.json", field = "your-custom-field", persist = true);
```
---
## file2.**`read`**
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
file2.read(file_uuid);
```
---
## file2.**`seek`**
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
file2.seek(file_uuid, 0);
```
---
## file2.**`open`**
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
file2.open(file_uuid);
```
---
## file2.**`is_open`**
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
file2.is_open(file_uuid);
```
---
## file2.**`exists`**
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
file2.exists(file_uuid);
```
---
## file2.**`write`**
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
file2.write(file_uuid, "your custom string");
```
---
## file2.**`flush`**
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
file2.flush(file_uuid);
```
---
## file2.**`close`**
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
file2.close(file_uuid);
```
---
## file2.**`detach`**
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
file2.detach(file_uuid);
```
---
## file2.**`delete`**
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
file2.delete(file_uuid);
```
---
## file2.**`attr`**
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
file2.attr(file_uuid);
```
---
## file2.**`to_bytes`**
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
file2.to_bytes(file_uuid);
```
---
## file2.**`to_base64`**
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
file2.to_base64(file_uuid);
```
---
## file2.**`to_json`**
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
file2.to_json(file_uuid);
```
---
## file2.**`dump_json`**
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
file2.dump_json(file_uuid, {"key": "value"});
```
---
## file2.**`download`**
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
file2.download("https://path/to/file", header={"Authorization":"key"});
```
---

# **`File Report`**
- dev can now report a file
    - `jsserv`: return the actual file
    - `jsctl`: return file2.attr (remote or local)
##### **`HOW TO TRIGGER`**
```js
report:file = uuid;
```
##### **`SAMPLE USAGE`**
```js
walker new_file {
    can file2.load;

    with entry {
        uuid = file2.load("testing.text");

        report:file = uuid;
    }
}
```
---

# **`Sample Codes`**

```python
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
        file2.dump_json(uuid, {"testing":1};

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

walker simple_with_file {
    has sample, fileTypeField;

    with entry {
        report sample;

        if fileTypeField and global.info['request_context']["body"]["ctx"]["fileTypeField"] {
            report true;
        }

        report fileTypeField[0];
        report file2.attr(fileTypeField[0]);
        report file2.read(fileTypeField[0], 0);
        report file2.to_json(fileTypeField[0]);
        report file2.to_bytes(fileTypeField[0]).str;
        report file2.to_base64(fileTypeField[0]);
    }
}

walker simple_custom_payload_with_file {
    has fileTypeField;

    can file2.attr, file2.read, file2.to_json, file2.to_base64, file2.to_bytes;

    with entry {
        if not fileTypeField and not global.info['request_context']["body"]["ctx"] {
            report true;
        }

        uuid = global.info['request_context']["body"]["fileTypeField"][0];
        report uuid;
        report file2.attr(uuid);
        report file2.read(uuid, 0);
        report file2.to_json(uuid);
        report file2.to_bytes(uuid).str;
        report file2.to_base64(uuid);
    }
}


```