import urllib.request
import json
import os
import sys

# Declare and initialize constants to represent the file paths for tags.txt
# (tag lists to download against) and files.dat (database of posts that have
# already been downloaded).
TAGS_TXT_FILE_PATH = os.path.join(os.getcwd(), "tags.txt")
FILES_DAT_FILE_PATH = os.path.join(os.getcwd(), "files.dat")

page = 1
limit = 75
tags = []
headers={'User-Agent':"Tag_Downloader"}
dbappend = []

# Read in tags from tags.txt. If tags.txt does not exist, create it and direct
# the user to populate the file with the tags they want to download against.
try:
    f = open(TAGS_TXT_FILE_PATH, 'r')
    tags = f.readlines()
    f.close()

    if not tags:
        raise ValueError
except:
    f = open(TAGS_TXT_FILE_PATH, 'w')
    f.close()
    print("No tag file found! The file has been created for you. Please type your search into tags.txt", file=sys.stderr)
    input("Press Enter to quit...")
    quit(-1)

# Prepare all tag lists for use in requests against e621 by replacing spaces
# with URL-encoded space ("%20") and stripping out newlines.
for index, item in enumerate(tags):
    tags[index] = item.replace(" ", "%20").replace("\n", "")

# Open the database of posts that have already been downloaded, or create
# it if it doesn't already exist.
try:
    f = open(FILES_DAT_FILE_PATH, 'r')
except:
    f = open(FILES_DAT_FILE_PATH, 'w')
    f.close()
    f = open(FILES_DAT_FILE_PATH, 'r')

# Read in the database of posts that have already been downloaded to
# reference during the download operation. If speed becomes an issue on
# larger databases, try sorting this and implementing a quicker search.
db = f.readlines()

# Close the database file (its contents are available as "db" to reference
# as the script continues running).
f.close()

# Iterate over the list of already downloaded posts to ensure that each
# post identifier is properly typed as an int.
for i in range(len(db)):
    db[i] = int(db[i])

# Iterate over the list of tag lists, requesting media from e621 matching each
# set of tags.
for tag_list in tags:
    # Reset page number to back to 1 to ensure that all pages are read and
    # processed when processing multiple tag lists.
    page = 1

    while True:
        # Build the request URL using the current tag list, page number, and
        # page post limit.
        url = "https://e621.net/posts.json?tags={}&page={}&limit={}".format(tag_list, page, limit)
        print(url)

        # Build and submit the HTTP request to e621 for processing.
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)

        # Read the response data in.
        data = response.read().decode('utf_8')

        # Deserialize return JSON for further processing.
        jsondata = json.loads(data)
        #print(jsondata["posts"])

        print(len(jsondata["posts"]))

        # If the request yielded no posts, continue to process the response
        # data.
        if len(jsondata["posts"]) == 0:
            break
        
        # Download each post in the returned page of posts.
        for i in range(len(jsondata["posts"])):
            # If the post is in the database of posts that have already been
            # download, skip the download step (and move on to the next post).
            if jsondata["posts"][i]["id"] in db:
                print("Post #" + str(jsondata["posts"][i]["id"]) + " already exists!")
                continue

            # Download the post, reporting details about the post as it's downloaded.
            print("Downloading post #" + str(jsondata["posts"][i]["id"]) + ".")
            print(i)
            print(jsondata["posts"][i]["file"])
            url = jsondata["posts"][i]["file"]["url"]
            if not url:
                md5 = jsondata["posts"][i]["file"]["md5"]
                url = "https://static1.e621.net/data/"+md5[0:2]+"/"+md5[2:4]+"/"+md5+"."+jsondata["posts"][i]["file"]["ext"]
            print(url)
            request=urllib.request.Request(url,None,headers)

            f = open(os.path.join(os.getcwd(), "downloads", str(jsondata["posts"][i]["id"]) + "." + jsondata["posts"][i]["file"]["ext"]), 'wb')
            f.write(urllib.request.urlopen(request).read())
            f.close

            # Add the post's identifier to a list of downloaded posts, which
            # will be added to the database of posts that have already been
            # downloaded later.
            dbappend.append(str(jsondata["posts"][i]["id"]))

        # Open the database of posts that have already been downloaded so the
        # set of newly-downloaded posts can be added to it.
        f = open(FILES_DAT_FILE_PATH, 'a')

        # Append the identifier for each newly-downloaded post to the database
        # of posts that have already been downloaded.
        for i in dbappend:
            f.write(i+"\n")
            print(i)
        
        # Close the database of posts that have already been downloaded.
        f.close()
        dbappend = []
        
        # Move on to request and process the next page of posts from e621.
        print("Next page.")
        page += 1

print("Done.")
