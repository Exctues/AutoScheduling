from Backend.Common import nl
import re

JSON_SlotStart = '{'
JSON_SlotEnd = '}'
JSON_SlotSeparator = r'\s*,\s*'  # assuming no commas inside values.
JSON_SlotInfoSeparator = r'\s*:\s*'
JSON_CourseNameId = 0
JSON_LessonTypeId = 1
JSON_TeacherId = 2
JSON_GroupId = 3
JSON_DayId = 4
JSON_TimeId = 5
JSON_RoomId = 6
JSON_SlotLength = 7
JSON_SlotInfoLength = 2
JSON_SlotInfoValue = 1
#                 number of info  info sep value         commas          {}  []
JSON_MinLength = JSON_SlotLength * (3 + 1 + 3) + (JSON_SlotLength - 1) + 2 + 2


# Errors in json.
class JSONException(Exception):
    pass


class SlotInfo:
    def __init__(self, name: str, typ: str, group: str, teacher: str, day: str, time: str, room: str):
        self.day = day
        self.time = time
        self.group = group
        self.name = name + ' ' + typ
        self.teacher = teacher
        self.room = room

    def getDay(self) -> str:
        return self.day

    def getTime(self) -> str:
        return self.time

    def getLabel(self) -> str:
        return self.name + nl + self.teacher + nl + self.room

    def __str__(self):
        return 'Day: ' + self.day + nl +\
               'Time: ' + self.time + nl +\
               'Group: ' + self.group + nl +\
               'What: ' + self.name + nl +\
               'Who: ' + self.teacher + nl + \
               'Where: ' + self.room + nl


class Schedule:
    def __init__(self, days: list, times: list, grades: dict, courses: list, teachers: list, rooms: list):
        self.days = days
        self.times = times
        self.grades = grades
        self.allGroups = []
        for l in grades.values():
            self.allGroups += l
        self.courses = courses
        self.teachers = teachers
        self.rooms = rooms
        self.slots = []

    def addSlots(self, slots: list):
        self.slots += slots

    def getDays(self) -> list:
        return self.days

    def getTimeSlots(self) -> list:
        return self.times

    def getGrades(self) -> dict:
        return self.grades

    def getGroupsOfGrade(self, grade: str) -> list:
        return self.grades[grade]

    def getSlotsOfGroup(self, group: str) -> list:
        return [slot for slot in self.slots if slot.group == group]


def ParseJSONSlotInfo(data: list, id: int, where: list = None, errmes: str = '') -> str:
    info = data[id]
    info = info[1:len(info) - 1]  # get rid of "
    if not (where is None or info in where):
        raise JSONException('JSON file has incorrect values: ' + errmes + ' ' + info + '.')
    return info


def ParseJSONSlot(table: Schedule, s: str) -> list:
    data = re.split(JSON_SlotSeparator, s)
    # Check if got slot is acceptable.
    if len(data) != JSON_SlotLength:
        raise JSONException('JSON file has incorrect format: a slot does not have some information.')
    for i in range(JSON_SlotLength):
        d = data[i]
        match = re.search(JSON_SlotInfoSeparator, d)
        if match is None:
            raise JSONException('JSON file has incorrect format: a slot information does not have a value.')
        data[i] = d[match.end():]
    # Parsing
    # name = ParseJSONSlotInfo(data, JSON_CourseNameId, table.courses, 'a slot has a nonexistent course')
    name = ParseJSONSlotInfo(data, JSON_CourseNameId)  # temporary
    typ = ParseJSONSlotInfo(data, JSON_LessonTypeId)
    # teacher = ParseJSONSlotInfo(data, JSON_TeacherId, table.teachers, 'a slot has a nonexistent teacher')
    teacher = ParseJSONSlotInfo(data, JSON_TeacherId)  # temporary
    day = ParseJSONSlotInfo(data, JSON_DayId, table.days, 'a slot has a nonexistent day')
    time = ParseJSONSlotInfo(data, JSON_TimeId, table.times, 'a slot has a nonexistent time')
    # room = ParseJSONSlotInfo(data, JSON_RoomId, table.rooms, 'a slot has a nonexistent room')
    room = ParseJSONSlotInfo(data, JSON_RoomId)  # temporary

    # Must be changed in future!
    group = ParseJSONSlotInfo(data, JSON_GroupId)
    if group in table.allGroups:
        return [SlotInfo(name, typ, group, teacher, day, time, room)]
    if group in table.grades:
        return [SlotInfo(name, typ, g, teacher, day, time, room) for g in table.grades[group]]
    raise JSONException('JSON file has incorrect values: a slot has a nonexistent group.')


def AddAlgoOutputToDS(json_path: str, table: Schedule):
    print("path=", json_path)
    with open(json_path, encoding='utf-8') as f:
        inp = f.read().strip()
    L = len(inp)
    if L < JSON_MinLength:
        raise JSONException('JSON file has incorrect format: too small length.')
    inp = inp[1:L - 1]
    to = 0
    while to < len(inp):
        inp = inp[to:]
        try:
            fr = inp.index(JSON_SlotStart) + 1
            to = inp.index(JSON_SlotEnd)
        except ValueError as e:
            raise JSONException('JSON file has incorrect format: ' + str(e) + '.')
        table.addSlots(ParseJSONSlot(table, inp[fr:to]))
        to += 1


def sample():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    times = ['09:00-10:30', '10:35-12:05', '12:10-13:40', '14:10-15:40', '15:45-17:15', '17:20-18:50', '18:55-20:25', '20:30-22:00']
    grades = dict()
    grades['BS17'] = ['BS17-0' + str(i) for i in range(1, 9)]
    grades['BS18'] = ['BS18-0' + str(i) for i in range(1, 9)]
    grades['B16-DS'] = ['B16-DS-01']
    table = Schedule(days, times, grades, list(), list(), list())
    try:
        AddAlgoOutputToDS('sample.json', table)
    except JSONException as e:
        print(e)
        return
    grades = table.getGrades()
    # print("grades=", grades)
    for k in grades:
        groups = table.getGroupsOfGrade(k)
        for g in groups:
            slots = table.getSlotsOfGroup(g)
            print("slots=", slots)
            for s in slots:
                print(s)


# sample()
