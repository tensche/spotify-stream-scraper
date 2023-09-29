import requests, urllib, time
from uuid import uuid4

session = requests.Session()
session.headers.update(
    {
        'authority': 'www.spotify.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
)


#GENERAL STUFF


def Cookies(session: requests.Session) -> int:
    r = session.get("https://www.spotify.com")
    return r.status_code

def CLIENT_Token(session: requests.Session) -> str:
    while True:
        payload = {
            'client_data': {
                'client_version': '11.2.20.3.g8d1df67e',
                'client_id': 'd8a5ed958d274c2e8ee717e6a4b0971d',
                'js_sdk_data': {
                    'device_brand': 'unknown',
                    'device_id': str(uuid4()),
                    'device_model': 'unknown',
                    'device_type': 'computer',
                    'os': 'windows',
                    'os_version': 'NT 10.0'
                }
            }
        }

        headers = {
            'authority': 'clienttoken.spotify.com',
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/json',
            'origin': 'https://open.spotify.com',
            'referer': 'https://open.spotify.com/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="116", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        r = session.post(url='https://clienttoken.spotify.com/v1/clienttoken', headers=headers, json=payload)

        if r.status_code == 200:
            return r.json()['granted_token']['token']
        else:
            print('Failed to get Client Token. Retrying...')

def CSRF_Token(session: requests.Session) -> str:
    while True:
        r = session.get(url='https://www.spotify.com/us/signup')

        if r.status_code == 200:
            return r.text.split('csrfToken')[1].split('"')[2]
        else:
            print('Failed to get CSRF-Token. Retrying...')

def BEARER_Token(session: requests.Session, CSRF: str) -> str:
    while True:   
        headers = {
            'authority': 'www.spotify.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.spotify.com',
            'referer': 'https://www.spotify.com/us/signup',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-csrf-token': CSRF,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        r1 = requests.post(url='https://www.spotify.com/api/signup/authenticate', headers=headers)

        if r1.status_code == 200:
            headers = {
                'authority': 'open.spotify.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

            r2 = session.get(url='https://open.spotify.com/get_access_token?reason=transport&productType=web_player', headers=headers)
            if r2.status_code == 200:
                return r2.json()['accessToken']
            else:
                print('Failed to get Access Token. Retrying...')
        else:
            print('Failed to authenticating account. Retrying...')


#ARTISTS


def RELEASE_IDS(session: requests.Session, BEARER_Token: str, CLIENT_Token: str, artist_url_encode: str) -> list:
    RELEASE_IDS = []
    url = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryArtistDiscographyAll&variables={artist_url_encode}&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2235a699e12a728c1a02f5bf67121a50f87341e65054e13126c03b7697fbd26692%22%7D%7D"

    headers = {
        "path": f"/pathfinder/v1/query?operationName=queryArtistDiscographyAll&variables={artist_url_encode}&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2246ae954ef2d2fe7732b4b2b4022157b2e18b7ea84f70591ceb164e4de1b5d5d3%22%7D%7D",
        "authorization": f"Bearer {BEARER_Token}",
        "client-token": CLIENT_Token
    }

    r = session.get(url, headers=headers)

    if r.status_code == 200:
        data = r.json()['data']['artistUnion']['discography']['all']

        for i in range(data['totalCount']):
            RELEASE_IDS.append(data['items'][i]['releases']['items'][0]['id'])
        return RELEASE_IDS
    else:
        print("failed to get release id's, artist is maybe banned")


def ARTIST_name(session: requests.Session, BEARER_Token: str, CLIENT_Token: str, artist_url_encode: str) -> str:
    url = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryArtistOverview&variables={artist_url_encode}&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2235648a112beb1794e39ab931365f6ae4a8d45e65396d641eeda94e4003d41497%22%7D%7D"

    headers = {
        "path": f"/pathfinder/v1/query?operationName=queryArtistOverview&variables={artist_url_encode}&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2235648a112beb1794e39ab931365f6ae4a8d45e65396d641eeda94e4003d41497%22%7D%7D",
        "authorization": f"Bearer {BEARER_Token}",
        "client-token": CLIENT_Token
    }

    r = session.get(url, headers=headers)
    return r.json()['data']['artistUnion']['profile']['name']


#RELEASE STATS


def RELEASE_STREAM_SCRAPER(session: requests.Session, BEARER_Token: str, CLIENT_Token: str, song_url_encode: str) -> str:
    global total
    while True:
        current_release = 0
        url = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=getAlbum&variables={song_url_encode}&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2246ae954ef2d2fe7732b4b2b4022157b2e18b7ea84f70591ceb164e4de1b5d5d3%22%7D%7D"

        headers = {
            "path": f"/pathfinder/v1/query?operationName=getAlbum&variables={song_url_encode}&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2246ae954ef2d2fe7732b4b2b4022157b2e18b7ea84f70591ceb164e4de1b5d5d3%22%7D%7D",
            "authorization": f"Bearer {BEARER_Token}",
            "client-token": CLIENT_Token
        }

        r = session.get(url, headers=headers)

        try:
            data = r.json()['data']['albumUnion']
            if data['__typename'] == "Album":
                songs = int(data['tracks']['totalCount'])
                for i in range(songs):
                    total += int(data['tracks']['items'][i]['track']['playcount'])
                    current_release += int(data['tracks']['items'][i]['track']['playcount'])

            elif data['__typename'] == "EP":
                songs = int(data['tracks']['totalCount'])
                for i in range(songs):
                    total += int(data['tracks']['items'][i]['track']['playcount'])
                    current_release += int(data['tracks']['items'][i]['track']['playcount'])

            elif data['__typename'] == "Single":
                total += int(data['tracks']['items'][0]['track']['playcount'])
                current_release += int(data['tracks']['items'][i]['track']['playcount'])

            song_name = data['name']
            return (song_name, current_release)
        except:
            print(r.status_code)
            # print(r.text)
            print("Failed to get data. Retrying...")
            time.sleep(2)

total = 0
artist = str(input(""))
artist_url = '{"uri":"spotify:artist:'+artist
artist_url += '","offset":0,"limit":100}'
artist_id = urllib.parse.quote(artist_url)

artist_url2 = '{"uri":"spotify:artist:'+artist
artist_url2 += '","locale":"intl-de","includePrerelease":true}'
artist_id2 = urllib.parse.quote(artist_url2)

Cookie = Cookies(session)
CSRF_str = CSRF_Token(session)
BEARER_str = BEARER_Token(session, CSRF_str)
CLIENT_str = CLIENT_Token(session)
RELEASE_list = RELEASE_IDS(session, BEARER_str, CLIENT_str, artist_id)
ARTIST_str = ARTIST_name(session, BEARER_str, CLIENT_str, artist_url2)

for i in RELEASE_list:

    release_url = '{"uri":"spotify:album:'+i
    release_url += '","locale":"intl-de","offset":0,"limit":100}'

    song_url_encode = urllib.parse.quote(release_url)
    data = RELEASE_STREAM_SCRAPER(session, BEARER_str, CLIENT_str, release_url)
    print(f"{data[0]} has {data[1]} streams")

print(f"{ARTIST_str} has {total} total streams")
