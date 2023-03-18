from datetime import datetime
import json
import requests
import time
import re
import copy
from sanic.log import logger

login_url = 'http://jwglweixin.bupt.edu.cn/bjyddx/login'
get_empty_classroom_url = 'http://jwglweixin.bupt.edu.cn/bjyddx/todayClassrooms?campusId=0'

userNo = '2019114514'
encoded_pwd = 'encoded_pwd'

token = None


def login():
    data = {
        'userNo': userNo,
        'pwd': encoded_pwd,
        'encode': '1',
        'captchaData': '',
        'codeVal': ''
    }
    r = requests.post(login_url, data=data)
    if r.status_code == 200 and r.json()['code'] == '1':
        global token
        token = r.json()['data']['token']
        return True
    return False


def get_empty_classroom(id):
    header = {
        'token': token
    }
    r = requests.get(get_empty_classroom_url+str(id), headers=header)
    if r.status_code == 200 and r.json()['code'] == '1':
        return r.json()['data']
    return []


def check():
    if login():
        empty_classroom = get_empty_classroom(1)
        class_list = []
        for each_class in empty_classroom:
            classroom_list = []
            class_room_raw = each_class['CLASSROOMS'].split(',')
            for each_room in class_room_raw:
                room_info = []
                room_info.append(
                    each_room.split('(')[0].replace(
                        '1-', '教1-').replace('2-', '教2-').replace('3-', '教3-').replace('4-', '教4-').replace('图书馆', '图书馆-'))
                room_info.append(each_room.split('(')[1].replace(')', ''))
                classroom_list.append(room_info)
            class_list.append(classroom_list)

        ans = {
            '1': copy.deepcopy(class_list)
        }

        empty_classroom = get_empty_classroom(4)
        class_list = []
        for each_class in empty_classroom:
            classroom_list = []
            class_room_raw = each_class['CLASSROOMS'].split(',')
            for each_room in class_room_raw:
                room_info = []
                room_info.append(
                    re.sub(r'^([S|N])(\d+)$', r'\1-\2', each_room.split('(')[0]))
                room_info.append(each_room.split('(')[1].replace(')', ''))
                classroom_list.append(room_info)
            class_list.append(classroom_list)
        ans['2'] = copy.deepcopy(class_list)

        ans['type_map'] = {}

        with open('classTable/config.json') as f:
            config = json.load(f)
        startWeek = config['startWeek']  # 2023-02-20
        nowWeek = int((datetime.now().timestamp(
        ) - datetime.strptime(startWeek, '%Y-%m-%d').timestamp()) / 604800) + 1
        today = datetime.now().weekday()

        with open('classTable/西土城路校区.json') as f:
            class_table = json.load(f)

        ans['type_map'] = class_table['typeMap']

        for class_list in class_table['class']:
            for each_classtime in range(14):
                if nowWeek not in class_list['classes'][each_classtime][today]:
                    ans['1'][each_classtime].append(
                        [class_list['name'], class_list['seat']])
        with open('classTable/沙河校区.json') as f:
            class_table = json.load(f)

        ans['type_map'].update(class_table['typeMap'])

        for class_list in class_table['class']:
            for each_classtime in range(14):
                if nowWeek not in class_list['classes'][each_classtime][today]:
                    ans['2'][each_classtime].append(
                        [class_list['name'], class_list['seat']])

        with open('class_room_list_in.json', 'w') as f:
            json.dump({
                'class_list': ans,
                'date': time.strftime('%Y-%m-%d %H时', time.localtime(time.time())),
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + str(time.time() % 1)[1:5]
            }, f, ensure_ascii=False)
        return ans

    else:
        print('login failed')
        logger.error('login failed')
