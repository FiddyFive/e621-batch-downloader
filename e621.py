import urllib.request
import json
import os
import sys

page = 1
limit = 75
tags = []
headers={'User-Agent':"Tag_Downloader"}
dbappend = []

try:
    f = open(os.getcwd()+"\\tags.txt", 'r')
    tags = f.readlines()[0]
    f.close()
    if not tags:
        raise ValueError
except:
    f = open(os.getcwd()+"\\tags.txt", 'w')
    f.close()
    print("No tag file found! The file has been created for you. Please type your search in to tags.txt", file=sys.stderr)
    input("Press Enter to quit...")
    quit(-1)

tags = tags.replace(" ", "%20")

try:
    f = open(os.getcwd()+"\\files.dat", 'r')
except:
    f = open(os.getcwd()+"\\files.dat", 'w')
    f.close()
    f = open(os.getcwd()+"\\files.dat", 'r')

#if speed becomes an issue on larger databases, try sorting this and implementing a quicker search.
db = f.readlines()
f.close()

for i in range(len(db)):
    db[i] = int(db[i])

while True:
    url = "https://e621.net/posts.json?tags={}&page={}&limit={}".format(tags,page,limit)
    print(url)
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf_8')

    jsondata = json.loads(data)
    #print(jsondata["posts"])

    print(len(jsondata["posts"]))

    if len(jsondata["posts"]) == 0:
        break
    
    for i in range(len(jsondata["posts"])):
        if jsondata["posts"][i]["id"] in db:
            print("Post #" + str(jsondata["posts"][i]["id"]) + " already exists!")
            continue

        print("Downloading post #" + str(jsondata["posts"][i]["id"]) + ".")
        print(i)
        print(jsondata["posts"][i]["file"])
        url = jsondata["posts"][i]["file"]["url"]
        if not url:
            md5 = jsondata["posts"][i]["file"]["md5"]
            url = "https://static1.e621.net/data/"+md5[0:2]+"/"+md5[2:4]+"/"+md5+"."+jsondata["posts"][i]["file"]["ext"]
        print(url)
        request=urllib.request.Request(url,None,headers)

        f = open(os.getcwd() + "\\downloads\\" + str(jsondata["posts"][i]["id"]) + "." + jsondata["posts"][i]["file"]["ext"], 'wb')
        f.write(urllib.request.urlopen(request).read())
        f.close

        dbappend.append(str(jsondata["posts"][i]["id"]))

    f = open(os.getcwd()+"\\files.dat", 'a')
    for i in dbappend:
        f.write(i+"\n")
        print(i)
    f.close()
    dbappend = []
    
    print("Next page.")
    page += 1

print("Done.")
