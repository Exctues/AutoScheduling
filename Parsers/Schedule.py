import json
from Parsers.Common import nl, LessonTypes


Key_course = 'Course_name'
Key_type = 'Lesson_type'
Key_teacher = 'Faculty'
Key_group = 'Group'
Key_day = 'Day'
Key_time = 'Time'
Key_room = 'Auditorium'


# Errors in json.
class JSONException(Exception):
    pass


def JSONErrorMessage(typ: str, what: str) -> str:
    return 'JSON file has incorrect values: a slot has a nonexistent ' + typ + ' ' + what + '.'


def CheckJSONInfo(info: str, where: list, typ: str):
    if not (info in where):
        raise JSONException(JSONErrorMessage(typ, info))


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

    def addSlot(self, slot: SlotInfo):
        self.slots.append(slot)

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

    def addDataFromJSON(self, path_to_json):
        with open(path_to_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for d in data:
            course, typ, group, teacher, day, time, room = \
                d[Key_course], d[Key_type], d[Key_group], d[Key_teacher], d[Key_day], d[Key_time], d[Key_room]
            CheckJSONInfo(course, self.courses, 'course')
            CheckJSONInfo(typ, LessonTypes, 'lesson type')
            CheckJSONInfo(teacher, self.teachers, 'teacher')
            CheckJSONInfo(day, self.days, 'day')
            CheckJSONInfo(time, self.times, 'time')
            CheckJSONInfo(room, self.rooms, 'room')

            if group in self.allGroups:
                self.addSlot(SlotInfo(course, typ, group, teacher, day, time, room))
            elif group in self.grades:
                self.addSlots([SlotInfo(course, typ, g, teacher, day, time, room) for g in self.grades[group]])
            else:
                raise JSONException(JSONErrorMessage('group', group))
