import requests
import spotipy
import spotipy.oauth2 as oauth2

client_id = "e17a6cc77e674b8180c6bb34f1b8ec7f"
client_secret = "415d0616f5154302b12a8c56741650b8"

auth = oauth2.SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = spotipy.Spotify(auth.get_access_token())


# info should be str containing artist album
def get_artwork(info):
    print("Attempting Art Retreival for: " + info)
    # takes second result first only because my initial test was Houses of The Holy.
    # Funny enough the song Houses of the holy returns first and is actually on Physical Graffiti, not the album Houses of the Holy

    if "houses of the holy" not in info.lower():
        img = sp.search(info)['tracks']['items'][0]['album']['images'][0]['url']
    else:
        img = sp.search(info)['tracks']['items'][1]['album']['images'][0]['url']

    # open img url and download image
    response = requests.get(img)

    # save image as file
    file = open("images/" + info.replace(" ", "-").replace("\n", "") + ".jpg", "wb")
    file.write(response.content)
    file.close()


def get_albums():
    # Open album list and iterate through
    f = open("AlbumList.txt")
    l = []
    while True:
        line = f.readline()
        # break loop when done so we don't try stupid shiz
        if not line:
            break
        # get art for every song and add it to list when exists
        get_artwork(line)
        l.append(line.replace(" ", "-").replace("\n", ""))
    f.close()
    return l
