import urllib.request
import json
import os

page = 1
limit = 5
tags = ""
headers={'User-Agent':"Anon"}
dbappend = []

try:
    f = open(os.getcwd()+"\\tags.txt", 'r')
except:
    f = open(os.getcwd()+"\\tags.txt", 'w')
    f.close()
    f = open(os.getcwd()+"\\tags.txt", 'r')

tags = f.readlines()[0]
f.close()

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
    url = "https://e621.net/post/index.json?tags={}&page={}&limit={}".format(tags,page,limit)
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf_8')
    if data == "[]":
        break

    jsondata = json.loads(data)

    print(len(jsondata))
    for i in range(len(jsondata)):
        if jsondata[i]["id"] in db:
            print("Post #" + str(jsondata[i]["id"]) + " already exists!")
            continue

        print("Downloading post #" + str(jsondata[i]["id"]) + ".")
        url = jsondata[i]["file_url"]
        request=urllib.request.Request(url,None,headers)

        f = open(os.getcwd() + "\\downloads\\" + str(jsondata[i]["id"]) + "." + jsondata[i]["file_ext"], 'wb')
        f.write(urllib.request.urlopen(request).read())
        f.close

        dbappend.append(str(jsondata[i]["id"]))

    f = open(os.getcwd()+"\\files.dat", 'a')
    for i in dbappend:
        f.write(i+"\n")
        print(i)
    f.close()
    dbappend = []
    
    print("Next page.")
    page += 1

print("Done.")
