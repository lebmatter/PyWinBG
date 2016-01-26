import json
import urllib2
import os
import random
import time
import urllib
import subprocess

JSON_IMAGE_FEED = "https://www.reddit.com/r/wallpapers/.json"
home = os.path.expanduser("~")
pic_folder = os.path.join(home, "Pictures")
pywinbg_folder = os.path.join(pic_folder, "PyWinBG")

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
    image_url = urllib2.urlopen(random_bg['data']['url'])
    if image_url.info().maintype == 'image':
        imgfile = urllib.URLopener()
        fname = '{}.jpg'.format(int(time.time()))
        download_path = os.path.join(pywinbg_folder, fname)
        try:
            imgfile.retrieve(image_url, download_path)
            return download_path
        except:
            get_random_image(itemlist)
    else:
        get_random_image(itemlist)

if not os.path.exists(pywinbg_folder):
    os.mkdir(pywinbg_folder)

url = urllib2.Request(JSON_IMAGE_FEED, headers = {'User-agent': 'helloworld9 0.1'})
bg_feed = json.load(urllib2.urlopen(url))
items = bg_feed['data']['children']
local_img = get_random_image(items)
# reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d  C:\users\image1.jpg /f
subprocess.call(['reg', 'add', '\"HKEY_CURRENT_USER\\Control Panel\\Desktop\"', '/v', 'Wallpaper', '/t', 'REG_SZ', '/d', local_img, '/f'])
subprocess.call(['%SystemRoot%\\System32\\RUNDLL32.EXE', 'user32.dll,UpdatePerUserSystemParameters'])
# %SystemRoot%\System32\RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters
