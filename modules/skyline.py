import requests
import json

SEARCH_API_KEY = "12061426-971bb3dbab06a0a8602a009a9"
SEARCH_URL = "https://pixabay.com/api/"


def get_skyline_link(city, country):
    """
    Extract the link to a skyline picture based off of a location.

    :param city: City to be searched.
    :param country: Country to be searched.
    :return: Link to the skyline picture.
    """

    params = {
        'key': SEARCH_API_KEY,
        'q': "{} skyline".format(city),
        'image_type': 'photo',
        'orientation': "horizontal",
        'searchType': "image"
    }
    response = requests.get(SEARCH_URL, params=params)

    if response.status_code != 200:
        return ""

    search_json = json.loads(response.content.decode('utf-8'))
    if search_json['totalHits'] == 0:
        return ""
    for hit in search_json["hits"]:
        return hit["largeImageURL"]
    return ""
