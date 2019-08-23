# import os
from time import sleep  # strftime
import requests
import datetime
import pymssql


def get_access_token(client_id, client_secret, refresh_token):
    """Returns access token of youtube api as a string.

    Idk what to write here.
    """
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


def get_streams_with_certain_statuses(api_key, access_token, statuses):
    """Returns all streams on some channel with certain status.

    Statuses can be: """

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json',
    }

    params = (
        ('part', 'snippet,contentDetails,status'),
        ('broadcastType', 'all'),
        ('mine', 'true'),
        ('key', api_key),
    )

    r = requests.get('https://www.googleapis.com/youtube/v3/liveBroadcasts', headers=headers, params=params)

    streams_data = {}
    if r.ok:
        for i, item in enumerate(r.json()['items']):
            if item['status']['lifeCycleStatus'] in statuses:
                streams_data[i] = {'title': item['snippet']['title'], 'id': item['id']}
    else:
        return None
    return streams_data


def stream_start(stream_id, api_key, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json',
    }

    params = (
        ('broadcastStatus', 'live'),
        ('id', stream_id),
        ('part', 'snippet,status'),
        ('key', api_key),
    )

    params2 = (
        ('broadcastStatus', 'testing'),
        ('id', stream_id),
        ('part', 'snippet,status'),
        ('key', api_key),
    )

    response = requests.post('https://www.googleapis.com/youtube/v3/liveBroadcasts/transition', headers=headers,
                             params=params)

    if str(response) == '<Response [200]>':
        print('Stream started! id = {}'.format(stream_id))
    else:
        print(requests.post('https://www.googleapis.com/youtube/v3/liveBroadcasts/transition', headers=headers,
                            params=params2), 'Changed to "Testing"')
        sleep(18)
        response = requests.post('https://www.googleapis.com/youtube/v3/liveBroadcasts/transition', headers=headers,
                                 params=params)
        if str(response) == '<Response [200]>':
            print('Stream started! id = {}'.format(stream_id), '(From "Testing")')
        else:
            print('SOMETHING WENT WRONG! START THE STREAM MANUALLY! ID = {}'.format(stream_id))
    return str(response)


def stream_stop(stream_id, api_key, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json',
    }

    params = (
        ('broadcastStatus', 'complete'),
        ('id', stream_id),
        ('part', 'snippet,status'),
        ('key', api_key),
    )

    response = requests.post('https://www.googleapis.com/youtube/v3/liveBroadcasts/transition', headers=headers,
                             params=params)

    if str(response) == '<Response [200]>':
        print('Stream stopped! id = {}'.format(stream_id))
    else:
        print('SOMETHING WENT WRONG! FINISH THE STREAM MANUALLY! ID = {}'.format(stream_id))


def find_last_start_db(channel_kind):
    with pymssql.connect('localhost', 'sa', '12345678', "AutoPlay7") as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT EventTime FROM dbo.AzSrvLogUsersInfo \
             where EventName LIKE '"+channel_kind+"' ORDER BY 'EventTime'")
            for row in cursor:
                last_event_time = row['EventTime']
            return last_event_time


def main(client_id, client_secret, api_key, refresh_token, channel_kind, lower_time_bracket):
    """its kinda documentary but I havent done it yet"""

    # Local Test
    '''
    client_id = '100199210836-jmgudguooe326e9iuka6c8hpj0cepv9e.apps.googleusercontent.com'
    client_secret = 'kQiWx0xORJLs0GtkJ_zhPOVD'
    refresh_token= '1/iKJd-5za3FVVOpu2NnnnRgt3DmVXSC9CXaO4MOUgAoY'
    api_key = 'AIzaSyDOfnp3ZnMb7WiIlG3OjY0rrq71PF4wZKs'
    '''

    access_token = get_access_token(client_id, client_secret, refresh_token)
    stream_id = ''
    Continue_Main = True

    while Continue_Main and datetime.datetime.now() <= lower_time_bracket + datetime.timedelta(minutes=2, seconds=1):
        last_start_time = find_last_start_db(channel_kind)

        if lower_time_bracket <= last_start_time <= lower_time_bracket + datetime.timedelta(minutes=2, seconds=1):
            streams_data = get_streams_with_certain_statuses(api_key, access_token, ['testing', 'ready'])

            for stream_data in streams_data:
                if streams_data[stream_data]['title'].find(lower_time_bracket.strftime("%m-%d")) != -1 and \
                        streams_data[stream_data]['title'].find((lower_time_bracket +
                                                                 datetime.timedelta(minutes=1)).strftime("%H:%M")) != -1:
                    stream_id = streams_data[stream_data]['id']

            start_status = stream_start(stream_id, api_key, access_token)
            Continue_Main = False

            if start_status == '<Response [200]>':
                Continue_Trying_To_Finish = True

                while Continue_Trying_To_Finish and \
                        datetime.datetime.now() <= lower_time_bracket + datetime.timedelta(minutes=57, seconds=1):
                    last_finish_time = find_last_start_db(channel_kind)

                    if last_start_time < last_finish_time:
                        stream_stop(stream_id, api_key, access_token)
                        Continue_Trying_To_Finish = False
                    else:
                        sleep(3)
        else:
            sleep(3)


if __name__ == "__main__":
    arr_timings = ['13:00/NEWS CENTRAL TV MD', '15:00/NEWS CENTRAL TV RU']
    #arr_timings1 = ['13:00/NEWS ORHEI TV MD', '15:00/NEWS ORHEI TV RU', '19:00/NEWS ORHEI TV MD',
    #               '21:00/NEWS ORHEI TV RU']

    while True:
        time_now = datetime.datetime.now()  # .strftime("%H:%M")
        time_after_minute = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")

        for arr_timing in arr_timings:
            if time_after_minute in arr_timing.split('/')[0]:
                client_id = '11035698848-dgvd84n9r3544vua5tuh45b1co5clueh.apps.googleusercontent.com'
                client_secret = 'TMcTfu5H2FyNB-7Ot8SPUZTw'
                api_key = 'AIzaSyBxuUbm2FnW42Ar3U-TXkMbbciCSn607CY'
                refresh_token = '1/5WP_Vd3GzbZ79pvKLLhWBfc05M_6XEevgIqfFpwnArxY4iY3QiPju8i0Cpiwgfqn'
                main(client_id, client_secret, api_key, refresh_token, arr_timing.split('/')[1], time_now)
        else:
            sleep(1)

'''

            for arr_timing in arr_timings1:
            if time_after_minute in arr_timing.split('/')[0]:
                cl_id = '11035698848-dgvd84n9r3544vua5tuh45b1co5clueh.apps.googleusercontent.com'
                cl_sec = 'TMcTfu5H2FyNB-7Ot8SPUZTw'
                api_key = 'AIzaSyBxuUbm2FnW42Ar3U-TXkMbbciCSn607CY'
                ref_tn = '1/5WP_Vd3GzbZ79pvKLLhWBfc05M_6XEevgIqfFpwnArxY4iY3QiPju8i0Cpiwgfqn'
                main(cl_id, cl_sec, api_key, ref_tn, arr_timing.split('/')[1], time_now)
        elif
    #Channel №2 (Orhei, old)
    client_id = '1001120855788-f4rbg0co31kt2lmalqic5t1ha6mp1k68.apps.googleusercontent.com'
    client_secret = '2xNqKdU_721IJg2ESb1wyQL6'
    refresh_token = '1/znQ4t6WBLealXD8FJXvWZF7jk0O6WP7pfMYYomaz6F17phpq70cWKFZnh8vYTiEF'
    api_key = 'AIzaSyCSt6stGMmadEV9qvI903HOcb6vWJO_nLo'
    #Channel №1 (Central)
    client_id = '11035698848-dgvd84n9r3544vua5tuh45b1co5clueh.apps.googleusercontent.com'
    client_secret = 'TMcTfu5H2FyNB-7Ot8SPUZTw'
    api_key = 'AIzaSyBxuUbm2FnW42Ar3U-TXkMbbciCSn607CY'
    refresh_token = '1/5WP_Vd3GzbZ79pvKLLhWBfc05M_6XEevgIqfFpwnArxY4iY3QiPju8i0Cpiwgfqn'
    

        '''
