import json
import xlrd


excludeBuilding = ['在线教学楼沙河', '教学实验综合楼', 'S1教学楼']
ignoreBuilding = ['在线教学楼沙河']
ignoreClassroom = ['虚拟教室']

filename = '海南校区.xls'


def xls2json():
    names = set()
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    classrooms = []
    curClassroom = {}
    typeMap = {}
    i = 0
    while i < table.nrows:
        curClassroom = {}
        classroomInfo = table.row_values(i + 1)[1]
        while classroomInfo.find('  ') != -1:
            classroomInfo = classroomInfo.replace('  ', ' ')
        classroomInfoList = classroomInfo.split(' ')
        curClassroom['campus'] = classroomInfoList[2].split('(')[1].split(')')[
            0]
        building = classroomInfoList[3].split(':')[1]
        if building in ignoreBuilding:
            i += 18
            continue
        flag = False
        for b in ignoreClassroom:
            if classroomInfoList[1].split(':')[1].startswith(b):
                flag = True
                break
        if flag:
            i += 18
            continue
        curClassroom['seat'] = classroomInfoList[4].split(':')[1]
        curClassroom['name'] = building + '-' + \
            classroomInfoList[1].split(':')[1].split('-')[-1]
        typeMap[curClassroom['name']] = classroomInfoList[2].split(':')[
            1].split('(')[0]
        rawClasses = [table.row_values(i + 3 + j)[1:] for j in range(14)]
        classes = []
        for oneClass in rawClasses:
            tmp = []
            for weekday in range(7):
                weeks = set()
                classesInOneTime = oneClass[weekday].split('节]')[:-1]
                for eachClass in classesInOneTime:
                    weekStr = eachClass.split(' ')[-1].split('周')[0]
                    weeksList = weekStr.split(',')
                    for a in weeksList:
                        if a.find('单') != -1 and a.find('-') != -1:
                            start = int(a.split('-')[0])
                            end = int(a.split('-')[1].split('单')[0])
                            for b in range(start, end + 1):
                                if b % 2 == 1:
                                    weeks.add(b)
                        elif a.find('双') != -1 and a.find('-') != -1:
                            start = int(a.split('-')[0])
                            end = int(a.split('-')[1].split('双')[0])
                            for b in range(start, end + 1):
                                if b % 2 == 0:
                                    weeks.add(b)
                        elif a.find('-') != -1:
                            start = int(a.split('-')[0])
                            end = int(a.split('-')[1])
                            for b in range(start, end + 1):
                                weeks.add(b)
                        else:
                            weeks.add(int(a))
                tmp.append(list(weeks))
            classes.append(tmp)
        curClassroom['classes'] = classes
        if building not in excludeBuilding:
            classrooms.append(curClassroom)
            names.add(curClassroom['name'])
        i += 18
    ans = {
        "class": classrooms,
        "typeMap": typeMap
    }
    with open('classTable/' + filename.split('.')[0] + '.json', 'w') as f:
        json.dump(ans, f, ensure_ascii=False)


if __name__ == '__main__':
    xls2json()
