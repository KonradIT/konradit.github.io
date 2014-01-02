import requests
import time, random
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'content-type': 'application/json',
    'x-csrf-token': 'undefined',
    'x-500px-source': 'Profile',
    'Origin': 'https://500px.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://500px.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers',
}

s = requests.Session()
s.get("https://500px.com/p/konraditurbe?view=photos", headers=headers)

data = '''{"operationName":"OtherPhotosQuery","variables":{"username":"konraditurbe","pageSize":20},"query":"query OtherPhotosQuery($username: String!, $pageSize: Int) {
  user: userByUsername(username: $username) {
    ...OtherPhotosPaginationContainer_user_RlXb8
    id
  }
}

fragment OtherPhotosPaginationContainer_user_RlXb8 on User {
  photos(first: $pageSize, privacy: PROFILE, sort: ID_DESC) {
    edges {
      node {
        id
        legacyId
        canonicalPath
        width
        height
        name
        isLikedByMe
        notSafeForWork
        photographer: uploader {
          id
          legacyId
          username
          displayName
          canonicalPath
          followedByUsers {
            isFollowedByMe
          }
        }
        images(sizes: [33, 35]) {
          size
          url
          jpegUrl
          webpUrl
          id
        }
        __typename
      }
      cursor
    }
    totalCount
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"}'''.replace("\n", "\\n")

response = s.post('https://api.500px.com/graphql', headers=headers, data=data)
printed_posts = []

for post in response.json().get("data").get("user").get("photos").get("edges"):

    p = post.get("node")
    r = requests.get(p.get("images")[1].get("url"), allow_redirects=True)
    open("./img/gallery/%s.jpg" % p.get("legacyId"), "wb").write(r.content)
    printed_posts.append({
        "src": "./img/gallery/%s.jpg" % p.get("legacyId"),
        "h": p.get("height"),
        "w": p.get("width")})
    time.sleep(random.randint(1, 2))

downloaded_paths = [p.get("src") for p in printed_posts]
for f in os.listdir("./img/gallery"):
    if ("./img/gallery/" + f) not in downloaded_paths:
      os.remove("./img/gallery/" + f)

with open("images.js", "w") as f:

    f.write("const instagramposts =")
    f.write(json.dumps(printed_posts,  sort_keys=True,
                        indent=4))
    f.write(";")
