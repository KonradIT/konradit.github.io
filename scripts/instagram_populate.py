from instascrape import *
import os
import random
import time
import sys
import requests
from fake_useragent import UserAgent
ua = UserAgent(cache=False)

replace_me = "var items = [];"

cookie = "" if len(sys.argv) < 2 else sys.argv[1]
print(cookie)
headers = {
    "user-agent": ua.random,
}

if cookie != "":
    headers["cookie"] = "sessionid=%s" % cookie
s = requests.Session()
ig_profile = Profile('https://www.instagram.com/konrad_iturbe/')
ig_profile.scrape(session=s, headers=headers)

posts = ig_profile.get_recent_posts()

printed_posts = []

for post in [post for post in posts if not post.is_video]:

    # if os.path.isfile("./img/gallery/%s.png" % post.shortcode): continue
    post.scrape(session=s, headers=headers)
    print(post.id, post.shortcode)
    post.download("./img/gallery/%s.png" % post.shortcode)
    printed_posts.append({
        "src": "./img/gallery/%s.png" % post.shortcode,
        "h": post.height,
        "w": post.width})
    time.sleep(random.randint(1, 10))

with open("images.js", "w") as f:

    f.write("const instagramposts =")
    f.write(json.dumps(printed_posts,  sort_keys=True,
                       indent=4))
    f.write(";")
