import requests
from bs4 import BeautifulSoup
import spotipy


USER_ID = "your own user id"

ENDPOINT = f"https://api.spotify.com/v1/users/{USER_ID}/playlists"

CLIENT_ID_SPOTIFY = "your own id"
CLIENT_SECRET_SPOTIFY = "your own secret"

time_to_travel = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

url = f"https://www.billboard.com/charts/hot-100/{time_to_travel}"

response = requests.get(url)
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")


# SCRAPING ARTISTS INFO
first_artist = soup.find("span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max "
                                            "u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block "
                                            "a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u"
                                            "-font-size-20@tablet").getText()


artists = soup.find_all("span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-"
                                       "line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-"
                                       "truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")

list_artists = [artist.getText() for artist in artists]

# joining first artist to the list of other 99 artists - nr. 1 has different css style
list_artists.insert(0, first_artist)
complete_list_artists = [name.replace("\t", "").replace("\n", "") for name in list_artists]

# SCRAPING TRACKS INFO
names_songs = soup.find_all("h3",
                            class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-"
                                   "0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height"
                                   "-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-"
                                   "width-330 u-max-width-230@tablet-only",
                            id="title-of-a-story")

list_of_names = [name.getText() for name in names_songs]


nr_one = soup.find("h3",
                   class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-"
                          "size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-"
                          "normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-"
                          "spacing-0028@tablet",
                   id="title-of-a-story").getText()

# joining nr_one song to the list of other 99 songs - nr. 1 has different css style
list_of_names.insert(0, nr_one)

complete_list_songs = [name.replace("\t", "").replace("\n", "") for name in list_of_names]


# MAKING NEW SPOTIFY PLAYLIST

authorization = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID_SPOTIFY, client_secret=CLIENT_SECRET_SPOTIFY,
                                            redirect_uri="http://example.com/", scope="playlist-modify-private")

get_token = authorization.get_access_token(as_dict=False)

headers = {
    "user_id": USER_ID,
    "Authorization": "Bearer " + get_token
}

params = {
    "name": f"Best 100 of {time_to_travel}",
    "public": False
}
response = requests.post(ENDPOINT, headers=headers, json=params).json()

PLAYLIST_ID = response["id"]

# GET SPOTIFY TRACKS URIS
uri_list = []

for x in range(len(complete_list_songs)):

    track_info = requests.get('https://api.spotify.com/v1/search',
                              headers={"Authorization": "Bearer " + get_token},
                              params={"q": f"track: {complete_list_songs[x]} artist: {complete_list_artists[x]}",
                                      "type": "track"})

    data = track_info.json()
    try:
        uri_track = (data["tracks"]["items"][0]["uri"])
    except IndexError:
        pass
    else:
        uri_list.append(uri_track)

# ADD TRACKS INTO NEW PLAYLIST

endpoint_add = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"

headers_add = {
    "Authorization": "Bearer " + get_token
}

data_add = {
    "uris": [track for track in uri_list]
}
add_response = requests.post(endpoint_add, headers=headers_add, json=data_add)
