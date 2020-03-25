import pandas
from math import isnan
import datetime
import pymssql

ip = 'localhost'
login = 'sa'
password = '12345678'
bd = "AutoPlay7"


def get_excel_ids_TVC(excel_file_name, sheet_name):
    pandas_excel_file = pandas.ExcelFile(excel_file_name)
    list_with_clip_ids = list()
    data_sheet = pandas.read_excel(pandas_excel_file, sheet_name, usecols='J')
    for i in range(160):
        if type(data_sheet.iloc[i][0]) is not str:
            if not isnan(data_sheet.iloc[i][0]):
                list_with_clip_ids.append(data_sheet.iloc[i][0])
        elif data_sheet.iloc[i][0] == "ID":
            break
    return list_with_clip_ids


def create_playlist(play_list_name):
    def dt_now_ins():
        return "'"+str(datetime.datetime.now())[:-3].replace(' ', 'T')+"'"

    with pymssql.connect(ip, login, password, bd) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO dbo.PlayLists VALUES ('"+play_list_name+"',"+dt_now_ins()+",0,"+dt_now_ins()+
                           ","+dt_now_ins()+",1 ,1 ,NULL ,1 ,NULL ,0 ,NULL)")
            playlist_id = cursor.lastrowid
            conn.commit()
    return playlist_id


def update_playlist_content(playlist_id, list_with_clip_ids):
    def dt_now_ins():
        return str(datetime.datetime.now())[:-3].replace(' ', 'T')

    conn = pymssql.connect(ip, login, password, bd)
    playlist_list_of_values = list()
    for i, clip_id in enumerate(list_with_clip_ids):
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT MarkIn, ClipDuration FROM dbo.Clips where ClipId = " + str(clip_id))
            for row in cursor:
                mark_in = row['MarkIn']
                duration = row['ClipDuration']
        playlist_list_of_values.append((playlist_id, i+1, 1, 1, dt_now_ins(), mark_in, duration, 1, 0, '', None, None, None,
                                        clip_id, None, None, None, None, None, None, 1, 0, 0, None, None, None))     # 0 to markIn, duration!!

    #print(playlist_list_of_values)

    with conn.cursor() as cursor:
        cursor.executemany("INSERT INTO dbo.PlayListContent VALUES (%d,%d,%d,%d,%s,%d,%d,%d,%d,%s,%s,%s,%s,\
        %d,%s,%s,%s,%s,%s,%s,%d,%d,%d,%s,%s,%s)", playlist_list_of_values)
        conn.commit()


update_playlist_content(create_playlist('Auto_Test_OTV1'), get_excel_ids_TVC('test_excel.xlsx', 'OTV'))
update_playlist_content(create_playlist('Auto_Test_TVC1'), get_excel_ids_TVC('test_excel.xlsx', 'TVC'))







        #print(cursor)

#print(list_with_clip_ids)




