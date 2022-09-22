import re
import shutil
from os import walk
import os
import subprocess

# open read me file
def main():
    readme = open("README.md", "r")
    try:
        summaryfile = open("docs/src/SUMMARY.md", "w")
    except FileNotFoundError:
        os.makedirs("docs/src")
    else:
         summaryfile = open("docs/src/SUMMARY.md", "w")

    summaryfile.write("")
    summaryfile.close()
    summaryfile = open("docs/src/SUMMARY.md", "a")
    summaryfile.write("# summary \n")

    lines = readme.readlines()
    for line in lines:
        if line.find("## Other Resources") != -1:
            break

        if line.find(".md#") != -1:
            continue

        if line.find("https") != -1:
            continue

        if line.find("##") != -1:
            line = line.replace("#", "", 1)
            summaryfile.write(line + "\n")

        else:
            summaryfile.write(line)
            fileinfo = processline(line)
            if fileinfo != False:
                repofile = open(fileinfo["link"], "r")
                repofileLines = repofile.readlines()
                docfileLink = "docs/src/" + fileinfo["link"]
                try:
                    docfile = open(docfileLink, "w")
                except FileNotFoundError:
                    editedPth = docfileLink
                    fileposition = editedPth.rfind("/")
                    editedPth = editedPth[0:fileposition]
                    os.makedirs(editedPth)

                docfile = open(docfileLink, "w")
                docfile.write("")
                docfile.close()
                docfile = open(docfileLink, "a")
                for line in repofileLines:
                    docfile.write(line)

                docfile.close()

    files = getImages("examples/CanoniCAI/images")
    generateAssests(files)
    files = getImages("support/guide/assets")
    generateAssests(files)
    files = getImages("support/codelabs/canonicai/images")
    generateAssests(files)


def processline(line):

    beginheading = line.find("[")
    endheading = line.find("]")

    heading = line[2 + 1 : 21]
    heading = line[beginheading + 1 : endheading]
    beginlink = line.find("(")
    endlink = line.find(")")
    if endlink == -1:
        return False

    link = line[beginlink + 1 : endlink]
    if link.find("https") != -1:
        return False
    else:

        return {"heading": heading, "link": link}


def generateAssests(files):

    for file in files:

        newAssetPath = "docs/src/" + file
        try:
            shutil.copy(file, newAssetPath)
        except FileNotFoundError:
            editedPth = newAssetPath
            fileposition = editedPth.rfind("/")
            editedPth = editedPth[0:fileposition]
            os.makedirs(editedPth)
            shutil.copy(file, newAssetPath)


# get image paths
def getImages(path=None):
    if path != None:
        f = []
        d = []
        x = 0
        for (dirpath, dirnames, filenames) in walk(path):
            while x < len(filenames):
                filenames[x] = path + "/" + filenames[x]
                x = x + 1
            f.extend(filenames)
            d.extend(dirnames)
            break

        if len(d) > 0:
            for directory in d:

                ImageDirectory = getImages(path + "/" + directory)
                f.extend(ImageDirectory)

        return f


def serveMdBook():
    try:
        subprocess.call(["mdbook", "build", "docs"])
    except:
        print("An Error occured while trying to build")

def createmdbookDocs():
    try:
        subprocess.call(["mdbook","init", "docs", "--ignore=none","--title=Jaseci Documentation"])
    except:
        print("errro occured")

def copyTheme(path):
    try:
        os.makedirs("docs/theme")
    except :
        print("error making theme folder")

    files = []
    for (dirpath, dirnames, filenames) in walk(path):
            files.extend(filenames)

    for file in files:
        docspath = "docs/theme/" + file
        sourcepath = "support/theme/" + file
        shutil.copy(sourcepath, docspath)


def editbookTOML():
    book = open("docs/book.toml","a")
    book.write("[build]\n")
    book.write("use-default-preprocessors = false\n")
    book.write("[preprocessor.links]\n")
    book.close()


    




createmdbookDocs()
print("book created")
main()
print("files generated")
copyTheme("support/theme")
print("theme copied")
serveMdBook()
print("Docs built")
editbookTOML()
print("BOOK.toml file edited")
