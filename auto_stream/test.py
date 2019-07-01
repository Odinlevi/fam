from time import strftime, sleep
import datetime
import requests

cl_id = '11035698848-dgvd84n9r3544vua5tuh45b1co5clueh.apps.googleusercontent.com'
cl_sec = 'TMcTfu5H2FyNB-7Ot8SPUZTw'
api_key = 'AIzaSyBxuUbm2FnW42Ar3U-TXkMbbciCSn607CY'
ref_tn = '1/5WP_Vd3GzbZ79pvKLLhWBfc05M_6XEevgIqfFpwnArxY4iY3QiPju8i0Cpiwgfqn'

def get_access_token(client_id, client_secret, refresh_token):
    params = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    authorization_url = "https://www.googleapis.com/oauth2/v4/token"

    r = requests.post(authorization_url, data=params)
    if r.ok:
        return r.json()['access_token']
    else:
        return None

def get_stream_id_with_certain_status(api_key, access_token):#, status):
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Accept': 'application/json',
    }

    params = (
        ('part', 'snippet,contentDetails,status'),
        ('broadcastType', 'all'),
        ('mine', 'true'),
        ('key', api_key),
    )

    r = requests.get('https://www.googleapis.com/youtube/v3/liveBroadcasts', headers=headers, params=params)

    if r.ok:
        print(r.json())
        '''for item in r.json()['items']:
            print(item)
            if item['status']['lifeCycleStatus'] == status:
                return item['id']
            else:
                return None
    else:
        return None'''
access_token = get_access_token(cl_id, cl_sec, ref_tn)
get_stream_id_with_certain_status(api_key, access_token)#, '')
