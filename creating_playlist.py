import requests
from scraping import scraping_website


def create_playlist(user_id, date_entry, token):
    endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    complete_list_artists = scraping_website(date_entry)[0]

    complete_list_songs = scraping_website(date_entry)[1]

    # MAKING NEW SPOTIFY PLAYLIST

    headers = {
        "user_id": user_id,
        "Authorization": "Bearer " + token,
    }

    params = {
        "name": f"Best 100 of {date_entry}",
    }
    response = requests.post(endpoint, headers=headers, json=params).json()

    playlist_id = response["id"]

    # GET SPOTIFY TRACKS URIS
    uri_list = []

    for x in range(len(complete_list_songs)):

        track_info = requests.get('https://api.spotify.com/v1/search',
                                  headers={"Authorization": "Bearer " + token},
                                  params={
                                      "q": f"track: {complete_list_songs[x]} artist: {complete_list_artists[x]}",
                                      "type": "track"
                                  })

        data = track_info.json()
        try:
            uri_track = (data["tracks"]["items"][0]["uri"])
        except IndexError:
            pass
        else:
            uri_list.append(uri_track)

    # ADD TRACKS INTO NEW PLAYLIST

    endpoint_add = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    headers_add = {
        "Authorization": "Bearer " + token
    }

    data_add = {
        "uris": [track for track in uri_list]
    }
    requests.post(endpoint_add, headers=headers_add, json=data_add)

