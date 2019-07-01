import os
from time import strftime, sleep
import requests
import datetime

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

def get_stream_id_with_certain_status(api_key, access_token, status):
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
        for item in r.json()['items']:
            if item['status']['lifeCycleStatus'] == status:
                return item['id']
            else:
                return None
    else:
        return None

def stream_start( _, api_key, access_token):
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Accept': 'application/json',
    }

    params = (
        ('broadcastStatus', 'complete'),
        ('id', stream_id),
        ('part', 'snippet,status'),
        ('key', api_key),
    )

    response = requests.post('https://www.googleapis.com/youtube/v3/liveBroadcasts/transition', headers=headers, params=params)

    if str(response) == '<Response [200]>':
        print('Stream stopped!')
    else:
        print('SOMETHING WENT WRONG! START THE STREAM MANUALLY!')

def stream_stop(stream_id, api_key, access_token):
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Accept': 'application/json',
    }

    params = (
        ('broadcastStatus', 'complete'),
        ('id', stream_id),
        ('part', 'snippet,status'),
        ('key', api_key),
    )

    response = requests.post('https://www.googleapis.com/youtube/v3/liveBroadcasts/transition', headers=headers, params=params)

    if str(response) == '<Response [200]>':
        print('Stream stopped!')
    else:
        print('SOMETHING WENT WRONG! FINISH THE STREAM MANUALLY!')

def check_db_status():
    

    return 'stop'

def main(cl_id, cl_sec, api_key, ref_tn, channel_kind, lower_time_bracket):
    # All info for the program usage
    #Local Test
    '''
    cl_id = '100199210836-jmgudguooe326e9iuka6c8hpj0cepv9e.apps.googleusercontent.com'
    cl_sec = 'kQiWx0xORJLs0GtkJ_zhPOVD'
    ref_tn= '1/iKJd-5za3FVVOpu2NnnnRgt3DmVXSC9CXaO4MOUgAoY'
    api_key = 'AIzaSyDOfnp3ZnMb7WiIlG3OjY0rrq71PF4wZKs'
    '''
    access_token = get_access_token(cl_id, cl_sec, ref_tn)
    
    last_start_time = find_last_start_db(s)
    if last_start_time >= lower_time_bracket or last_start_time <= lower_time_bracket+datetime.timedelta(minutes=2, seconds=1):
        
    
    #stream_id = get_stream_id(api_key, access_token)
    #db_status = check_db_status()
    
    #if stream_id != None and db_status == 'Stop':
        #stream_stop(stream_id, api_key, access_token)
    

if __name__ == "__main__":
    # Time when the stream is shutting down
    arr_timings2 = ['12:00/NEWS CENTRAL TV MD', '14:00/NEWS CENTRAL TV RU', '18:00/NEWS CENTRAL TV MD', '20:00/NEWS CENTRAL TV RU']
    arr_timings1 = ['13:00/NEWS ORHEI TV MD', '15:00/NEWS ORHEI TV RU', '19:00/NEWS ORHEI TV MD', '21:00/NEWS ORHEI TV RU']
    while True:
        time_now = datetime.datetime.now()#.strftime("%H:%M")
        time_after_minute = (datetime.datetime.now()+datetime.timedelta(minutes=1)).strftime("%H:%M")
        if time_after_minute in arr_timings1.split('/')[0]:
            cl_id = '11035698848-dgvd84n9r3544vua5tuh45b1co5clueh.apps.googleusercontent.com'
            cl_sec = 'TMcTfu5H2FyNB-7Ot8SPUZTw'
            api_key = 'AIzaSyBxuUbm2FnW42Ar3U-TXkMbbciCSn607CY'
            ref_tn = '1/5WP_Vd3GzbZ79pvKLLhWBfc05M_6XEevgIqfFpwnArxY4iY3QiPju8i0Cpiwgfqn'
            main(cl_id, cl_sec, api_key, ref_tn, arr_timings1.split('/')[1], time_now)
        elif time_after_minute in arr_timings2.split('/')[0]:
            cl_id = '1001120855788-f4rbg0co31kt2lmalqic5t1ha6mp1k68.apps.googleusercontent.com'
            cl_sec = '2xNqKdU_721IJg2ESb1wyQL6'
            ref_tn = '1/znQ4t6WBLealXD8FJXvWZF7jk0O6WP7pfMYYomaz6F17phpq70cWKFZnh8vYTiEF'
            api_key = 'AIzaSyCSt6stGMmadEV9qvI903HOcb6vWJO_nLo'
            main(cl_id, cl_sec, api_key, ref_tn , arr_timings1.split('/')[1], time_now)
        else:
            sleep(10)
        


        '''
            рамка +- минута, старт за минуту до
                старт : поиск записи в базе о старте
                    если в базе запись, время которой не отличается больше чем на минуту от ЭТОЙ секунды,
                        поиск запланированного стрима, название которого СОДЕРЖИТ И время, И день
                            если такой стрим есть, перевод его в лайв
                            если нет, ВЫХОД С ОШИБКОЙ
                    если не прошло двух минут и одной секунды, спим 10 сек
                    иначе BREAK
        





    #Channel №2
    cl_id = '1001120855788-f4rbg0co31kt2lmalqic5t1ha6mp1k68.apps.googleusercontent.com'
    cl_sec = '2xNqKdU_721IJg2ESb1wyQL6'
    ref_tn = '1/znQ4t6WBLealXD8FJXvWZF7jk0O6WP7pfMYYomaz6F17phpq70cWKFZnh8vYTiEF'
    api_key = 'AIzaSyCSt6stGMmadEV9qvI903HOcb6vWJO_nLo'
    #Channel №1
    cl_id = '11035698848-dgvd84n9r3544vua5tuh45b1co5clueh.apps.googleusercontent.com'
    cl_sec = 'TMcTfu5H2FyNB-7Ot8SPUZTw'
    api_key = 'AIzaSyBxuUbm2FnW42Ar3U-TXkMbbciCSn607CY'
    ref_tn = '1/5WP_Vd3GzbZ79pvKLLhWBfc05M_6XEevgIqfFpwnArxY4iY3QiPju8i0Cpiwgfqn'
    

        '''
