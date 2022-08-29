import re
# open read me file 
def main():
    readme = open("README.md","r")
    summaryfile = open("documentation/src/SUMMARY.md","w")
    summaryfile.write("")
    summaryfile.close()
    summaryfile  = open("documentation/src/SUMMARY.md","a")
    summaryfile.write("# summary \n")

    lines =  readme.readlines()
    for line in lines:
        if line.find("## Other Resources") != -1:
            break
            
        if line.find(".md#") != -1:
            continue 
        
        if line.find("https") != -1:
            continue 
        

        if line.find("##"):
            summaryfile.write(line + "\n")

        else :
            summaryfile.write(line)
            fileinfo = processline(line)
            if fileinfo != False:
                repofile = open(fileinfo['link'],"r")
                repofileLines = repofile.readlines()
                docfileLink = "documentation/src/" + fileinfo['link']
                docfile = open(docfileLink,"w")
                docfile.write("")
                docfile.close()
                docfile = open(docfileLink, "a")
                for line in repofileLines:
                    docfile.write(line + "\n")

                docfile.close()



        


def processline(line):


    beginheading = line.find("[")
    endheading = line.find("]")

    heading = line[2+1:21]
    heading = line[beginheading+1:endheading]
    beginlink = line.find("(")
    endlink = line.find(")")
    if endlink == -1 :
        return False

    link = line[beginlink+1:endlink]
    if link.find("https") != -1:
        return False
    else:
        
        return {"heading": heading , "link" : link}
   
    

#def getLink():

main()
