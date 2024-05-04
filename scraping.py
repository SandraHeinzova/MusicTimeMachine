import requests
from bs4 import BeautifulSoup


def scraping_website(time_to_travel):
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

    return complete_list_artists, complete_list_songs


