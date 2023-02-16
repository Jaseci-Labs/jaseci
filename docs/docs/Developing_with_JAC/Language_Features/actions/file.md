# File Actions
### Load file to string
```jac
# Converts file to string , max_chars is set to none by default
Testfile = file.load_str(test.txt, max_chars = 1000)
```
### Load Json file to dictionary
```jac
# Loads json from file to dictionary format
TestJson = file.load_json(test.json)
```
### String to file
```jac
# dumps string in to file
test = "This is a test of the dump_str method
Testfile = file.dump_str("text.txt",test)
```
### Append string to a file
```jac
# appending a string to a file.
test = "This is a another test but with  the append_str method
Testfile = file.append_str(str, max_chars = 1000)
```

### Create Json File
```jac
# dump dictionary in to json file
test = {
    "name": "test",
    "method" : "dump_json",
    "use" : "dumps dictionary to json file"
}
Testfile = file.dump_json("text.json",test)
```
### Delete file
```jac
#delete any file
file.delete("text.txt")
```

### Example

```jac
walker init {
    fn="fileiotest.txt";
    a = {'a': 5};
    file.dump_json(fn, a);
    b=file.load_json(fn);
    b['a']+=b['a'];
    file.dump_json(fn, b);
    c=file.load_str(fn);
    file.append_str(fn, c);
    c=file.load_str(fn);
    report c;
}
```