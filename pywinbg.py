import json
import urllib2
import os
import random
import time
import subprocess

JSON_IMAGE_FEED = "https://www.reddit.com/r/wallpapers/.json"
home = os.path.expanduser("~")
pic_folder = os.path.join(home, "Pictures")
pywinbg_folder = os.path.join(pic_folder, "PyWinBG")
local_img = ''
# def imgur_resolver(imgurl):
#     '''
#     A dirty resolver to get direct imgur urls!
#     '''
#     if "i.imgur.com" in imgurl:
#         return imgurl
#     elif "http://imgur.com/gallery" in imgurl:
#         # Can't do anything if link is a gallery. Oops!
#         return None
#     elif "imgur.com" in imgurl:
#         return "{}.jpg".format(imgurl)
#     else:
#         # For all other urls
#         return None

def get_random_image(itemlist):
    random_bg = random.choice(itemlist)
    random_url = random_bg['data']['url']
    image_url = urllib2.urlopen(random_url)
    if image_url.info().maintype == 'image':
        print "Yaay! Found one at: {}".format(random_url)
        fname = '{}.jpg'.format(int(time.time()))
        download_path = os.path.join(pywinbg_folder, fname)
        print "Downloading with urllib2..."
        f = urllib2.urlopen(random_url)
        data = f.read()
        with open(download_path, "wb") as code:
            code.write(data)
        download_path = os.path.join(pywinbg_folder, fname)
        print "Saved image to: {}".format(download_path)
        global local_img
        local_img = download_path
    else:
        get_random_image(itemlist)

if not os.path.exists(pywinbg_folder):
    os.mkdir(pywinbg_folder)

print "Checking --r/Wallpapers-- for a fresh background!"
# If User-agent not changed, Reddit most probably gives you HTTP 429 Error.
url = urllib2.Request(JSON_IMAGE_FEED, headers = {'User-agent': 'PyWinBG 0.1'})
bg_feed = json.load(urllib2.urlopen(url))
items = bg_feed['data']['children']
get_random_image(items)
print "Changing Windows Background image..."
# Why we need a bat file to run instead of using subprocess directly?
# No idea! It was crashing if i change registry entry through subprocess!
subprocess.call(['regchanger.bat', local_img])
print "Done!"
