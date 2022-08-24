# code testing



```jac

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

```c
c = "cow";
```
```zenscript

print("Hello world!");

```