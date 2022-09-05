# code testing



```python

def generatedocs(title,fileList):
    AppendtoSummaryFile(title=title)
    for file in fileList:
        markdownFile = open(file['path'],"r")
        newpath = 'documentation/src/' + file['path']
        markdownFileLines = markdownFile.readlines()
        AppendtoSummaryFile(fileName= file['name'],path = file['path'],heading=file['heading'])
        newMarkdown = open(newpath,"w")
        newMarkdown.write("")
        newMarkdown.close()
        newMarkdown = open(newpath,"a")
        for lines in markdownFileLines:
            newMarkdown.write(lines)
        newMarkdown.close()

    print(title + "  section is completed")
```


```javascript
<!DOCTYPE html>
<html>
<body>

<h2>JavaScript Objects</h2>

<p>There are two different ways to access an object property.</p>

<p>You can use person.property or person["property"].</p>

<p id="demo"></p>

<script>
// Create an object:
const person = {
  firstName: "John",
  lastName : "Doe",
  id     :  5566
};

// Display some data from the object:
document.getElementById("demo").innerHTML =
person.firstName + " " + person.lastName;
</script>

</body>
</html>






```