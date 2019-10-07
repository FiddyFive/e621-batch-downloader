# e621-batch-downloader
A single, simple, out of the box python file to mass download e621 images.

The only requirement is Python 3.

To use, simply extract the files, delete downloads/deleteme.txt and edit tags.txt to your liking. 
In tags.txt type, in a single line, the tags as you would type them in e621.
Now run e621.py

This will create a file called files.dat.
files.dat keeps a record of downloaded images to save time in future uses. Delete this file for a clean run.

Note that e621 throttles users that make large numbers of requests, as a result downloads will massively slow down after downloading enough files. There is nothing I can do about this.
