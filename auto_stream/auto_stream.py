from time import sleep
import requests
import datetime
import pymssql
import passwords_file


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
        ('maxResults', '50'),
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
    print(streams_data)
    return streams_data


def stream_change_status(stream_id, api_key, access_token, status):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json',
    }

    params = (
        ('broadcastStatus', status),
        ('id', stream_id),
        ('part', 'snippet,status'),
        ('key', api_key),
    )

    response = requests.post('https://www.googleapis.com/youtube/v3/liveBroadcasts/transition', headers=headers,
                             params=params)
    if status == 'complete':
        if str(response) == '<Response [200]>':
            print('Stream stopped! id = {}'.format(stream_id))
        else:
            print('SOMETHING WENT WRONG! FINISH THE STREAM MANUALLY! ID = {}'.format(stream_id))
    elif status == 'live':
        if str(response) == '<Response [200]>':
            print('Stream started! id = {}'.format(stream_id))
        else:
            print('SOMETHING WENT WRONG! START THE STREAM MANUALLY! ID = {}'.format(stream_id))
    else:
        print('Changing ID {} to "Testing"'.format(stream_id))
    return str(response)


def find_last_start_db(channel_kind):
    ip = 'localhost'
    login = 'sa'
    password = '12345678'
    bd = "AutoPlay7"
    with pymssql.connect(ip, login, password, bd) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT EventTime FROM dbo.AzSrvLogUsersInfo \
             where EventName LIKE '"+channel_kind+"' ORDER BY 'EventTime'")
            for row in cursor:
                last_event_time = row['EventTime']
            return last_event_time


def main(client_id, client_secret, api_key, refresh_token, channel_and_time, lower_time_bracket):
    """its kinda documentary but I havent done it yet"""

    access_token = get_access_token(client_id, client_secret, refresh_token)
    stream_id = ''
    Continue_Main = True

    streams_data = get_streams_with_certain_statuses(api_key, access_token, ['testing', 'ready'])
    for stream_data in streams_data:
        if streams_data[stream_data]['title'].find(lower_time_bracket.strftime("%m-%d")) != -1 and \
                streams_data[stream_data]['title'].find(channel_and_time.split('/')[0]) != -1:
            stream_id = streams_data[stream_data]['id']
            break
    stream_change_status(stream_id, api_key, access_token, 'testing')

    print('Start scanning DB')
    while Continue_Main and datetime.datetime.now() <= lower_time_bracket + datetime.timedelta(minutes=4, seconds=1):
        last_start_time = find_last_start_db(channel_and_time.split('/')[1])
        if lower_time_bracket <= last_start_time <= lower_time_bracket + datetime.timedelta(minutes=4, seconds=1):
            print("DB insertion detected! Founded stream: https://www.youtube.com/watch?v={}".format(stream_id))

            start_status = stream_change_status(stream_id, api_key, access_token, 'live')
            Continue_Main = False

            if start_status == '<Response [200]>':
                Continue_Trying_To_Finish = True
                print("Start scanning DB (for stream's finishing).")
                while Continue_Trying_To_Finish and \
                        datetime.datetime.now() <= lower_time_bracket + datetime.timedelta(minutes=57, seconds=1):
                    last_finish_time = find_last_start_db(channel_and_time.split('/')[1])

                    if last_start_time < last_finish_time:
                        print('Stream will be finished in 20 seconds')
                        sleep(20)
                        stream_change_status(stream_id, api_key, access_token, 'complete')
                        Continue_Trying_To_Finish = False
                    else:
                        sleep(1)
                        print('Still scanning...')
        else:
            sleep(1)
            print('Still scanning...')
    else:
        print('Waiting for the next stream...')


if __name__ == "__main__":
    arr_timings = ['13:00/NEWS CENTRAL TV MD', '15:00/NEWS CENTRAL TV RU', '19:00ro', '20:00ru']
    #arr_timings1 = ['13:00/NEWS ORHEI TV MD', '15:00/NEWS ORHEI TV RU', '19:00/NEWS ORHEI TV MD',
    #               '21:00/NEWS ORHEI TV RU']

    while True:
        time_now = datetime.datetime.now()  # .strftime("%H:%M")
        time_after_two_minutes = (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime("%H:%M")

        for arr_timing in arr_timings:
            if time_after_two_minutes in arr_timing.split('/')[0]:
                main(passwords_file.client_id, passwords_file.client_secret, passwords_file.api_key,
                     passwords_file.refresh_token, arr_timing, time_now)
        else:
            sleep(3)
            print(datetime.datetime.now())

