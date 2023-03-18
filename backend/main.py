import sanic.response
import logging
import sanic
from get_classroom import check
import json
import time
from sanic.log import logger
logging.basicConfig(
    filename="ec.log", format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")


app = sanic.Sanic('get_classroom')

admin_pwd = "password"


class_list = {}


@app.route('/api')
async def get_room(request):
    global class_list
    try:
        if class_list != {}:
            if class_list['date'] != time.strftime('%Y-%m-%d %H时', time.localtime()):
                raise Exception('date not match')
        else:
            with open('class_room_list.json', 'r') as f:
                class_list = json.load(f)
                if class_list['date'] != time.strftime('%Y-%m-%d %H时', time.localtime()):
                    raise Exception('date not match')
    except:
        class_list = {
            'class_list': check(),
            'date': time.strftime('%Y-%m-%d %H时', time.localtime(time.time())),
            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + str(time.time() % 1)[1:5]
        }
        with open('class_room_list.json', 'w') as f:
            json.dump(class_list, f, ensure_ascii=False)
        try:
            with open("notification.json", "r") as f:
                notification = json.load(f)
                start = time.strptime(
                    notification["start"], "%Y-%m-%d %H:%M:%S")
                end = time.strptime(notification["end"], "%Y-%m-%d %H:%M:%S")
                if start < time.localtime() and time.localtime() < end:
                    class_list['notification'] = notification
        except:
            pass
        try:
            with open("version.json", "r") as f:
                tmp = json.load(f)
                class_list['version'] = tmp['version']
        except Exception as e:
            pass
        return sanic.response.json(class_list)
        # set cache control to 30 minutes
        # return sanic.response.json(class_list, headers={'Cache-Control': 'max-age=1800'})

    try:
        with open("notification.json", "r") as f:
            notification = json.load(f)
            start = time.strptime(notification["start"], "%Y-%m-%d %H:%M:%S")
            end = time.strptime(notification["end"], "%Y-%m-%d %H:%M:%S")
            if start < time.localtime() and time.localtime() < end:
                class_list['notification'] = notification
    except:
        pass
    try:
        with open("version.json", "r") as f:
            tmp = json.load(f)
            class_list['version'] = tmp['version']
    except Exception as e:
        pass
    return sanic.response.json(class_list)
    # return sanic.response.json(class_list, headers={'Cache-Control': 'max-age=1800'})


@app.post('/api/get-log')
async def getLog(request):
    try:
        if (request.args['pwd'][0] == admin_pwd):
            size = 100
            try:
                size = request.args['size'][0]
            except:
                size = 100
            with open('ec.log', "r") as f:
                return sanic.response.text("\n".join(f.readlines()[-100:]))
    except Exception as e:
        return sanic.response.empty(status=401)
    return sanic.response.empty(status=401)


def check_in_loop():
    logger.info('check in loop at ' +
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    global class_list
    class_list = {
        'class_list': check(),
        'date': time.strftime('%Y-%m-%d %H时', time.localtime(time.time())),
        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + str(time.time() % 1)[1:5]
    }
    with open('class_room_list.json', 'w') as f:
        json.dump(class_list, f, ensure_ascii=False)


def loop_check():
    while True:
        try:
            check_in_loop()
            delay = time.mktime(time.strptime(time.strftime('%Y-%m-%d %H:%M:01',
                                                            time.localtime(time.time() + 62)), '%Y-%m-%d %H:%M:%S')) - time.time()
            if delay < 1:
                delay = 10
            logger.info('next check in: ' + str(delay))
            time.sleep(delay)
        except Exception as e:
            logger.error(repr(e))
            time.sleep(60)


if __name__ == '__main__':
    import threading
    t = threading.Thread(target=loop_check)
    t.start()
    app.run(port=8856, debug=False, access_log=False)
