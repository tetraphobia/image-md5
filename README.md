# Image MD5
A small python script that takes images, generates an MD5 has from it's bytestrings,
renames the image to it's md5 hash, and outputs it to another directory. Optionally,
the script will run wpgtk on the images to generate colorschemes from them.


### Basic Usage
```bash
$ pip install -r requirements.txt
$ ./convert.py -w -o output/directory/foo/bar/ image1.png image.jpg image3.png
```
