import requests
import json

URL = 'https://www.googleapis.com/youtube/v3/search'
API_KEY = 'AIzaSyC5RDfdAuXqtRyr8KVcyTMIzl3WIpTWgLo'


def process_result(result):
    if 'id' not in result:
        return None
    if 'snippet' not in result:
        return None
    if 'videoId' not in result['id']:
        return None
    new_result = {
        'url': "https://youtube.com/watch?v=" + result['id']['videoId'],
        'embed_url': "https://www.youtube.com/embed/" + result['id']['videoId'] + "?enablejsapi=1&html5=1",
        'title': result['snippet']['title'],
        'thumbnail': result['snippet']['thumbnails']['default']['url']
    }
    return new_result


def video_search_query(query):
    params = {
        'part': 'snippet',
        'key': API_KEY,
        'maxResults': 25,
        'q': query
    }
    response = requests.get(URL, params=params)
    if response.status_code != 200:
        return None, "Search query did not go through!"
    else:
        raw_json = json.loads(response.content.decode('utf-8'))
        results = map(process_result, raw_json['items'])
        results = list(filter(lambda x: x is not None, results))
        return results, ""
