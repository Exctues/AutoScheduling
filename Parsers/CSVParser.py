import re
from Parsers.Schedule import Schedule
from Parsers.Common import LessonTypes

delimiter = ','
subdelimeter = r'\s*;\s*'


class Row:
    counter = -1
    objects = []

    def __init__(self, key: str, independent: bool = True, skip: int = 0):
        Row.counter += 1 + skip
        self.row = Row.counter
        self.key = key
        self.independent = independent
        Row.objects.append(self)


Days = Row('days')
Time = Row('time')

Rooms = Row('rooms', skip=1)
RoomCapacity = Row('roomcap', False)

Instructors = Row('teachers', skip=1)
BadDays = Row('baddays', False)
BadSlots = Row('badslots', False)

Groups = Row('groups', skip=1)
StudentsN = Row('studentsN', False)

Grades = Row('spec', skip=1)
GradeGroups = Row('gradegroups', False)

Course = Row('course', skip=1)
LessonType = Row('type', False)
GradeOrGroups = Row('grg', False)
Instructor = Row('ins', False)
LessonsN = Row('lesn', False)


# Wrap In Quotes.
def wiq(s: str) -> str:
    return '"' + s + '"'


# Wrap In Square Brackets.
def wisb(s: str) -> str:
    return '[' + s + ']'


# Make JSON key.
def mjsonk(name: str, values: list) -> str:
    return wiq(name) + ':' + wisb(','.join(values))


def BuildOneValueKey(name: str, values: list) -> str:
    temp = []
    for v in values:
        temp.append(wisb(wiq(v)))
    return mjsonk(name, temp)


def BuildTwoValueKey(name: str, values1: list, values2: list) -> str:
    temp = []
    for i in range(len(values1)):
        temp.append(wisb(wiq(values1[i]) + ',' + wiq(values2[i])))
    return mjsonk(name, temp)


# Mistakes in input file.
class CSVException(Exception):
    pass


def DefCSVException(row: int):
    raise CSVException('Input file has incorrect format in row ' + str(row + 1) + '.')


def ParseLine(line: str, row: int) -> list:
    temp = line.strip().split(delimiter)[1:]
    i = len(temp) - 1
    try:
        while temp[i] == '':
            i -= 1
    except IndexError:
        DefCSVException(row)
    temp = temp[:i + 1]
    if '' in temp:
        DefCSVException(row)
    return temp


def ParseLineWithBound(line: str, l: int) -> list:
    return line.strip().split(delimiter)[1:l + 1]


def ParseCSV(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        inp = f.readlines()
    info = dict()
    L = 0
    for r in Row.objects:
        if r.independent:
            info[r.key] = ParseLine(inp[r.row], r.row)
            L = len(info[r.key])
            if L == 0:
                DefCSVException(r.row)
        else:
            info[r.key] = ParseLineWithBound(inp[r.row], L)
            if len(info[r.key]) != L:
                DefCSVException(r.row)
    return info


def CheckIntList(ints: list, errmesfunct):
    for i in range(len(ints)):
        try:
            a = int(ints[i])
        except ValueError:
            raise CSVException(errmesfunct(i))
        if a <= 0:
            raise CSVException(errmesfunct(i))


def CheckPresenceInList(suspect: list, where: list, errmesfunct):
    for i in range(len(suspect)):
        if not (suspect[i] in where):
            raise CSVException(errmesfunct(i))


def ParseGroups(suspect: list, groups: list, errmesfunct_no_groups, errmesfunct) -> list:
    out = []
    for i in range(len(suspect)):
        s = suspect[i]
        if s == '':
            raise CSVException(errmesfunct_no_groups(i))
        s = re.split(subdelimeter, s)
        for g in s:
            if not (g in groups):
                raise CSVException(errmesfunct(i, g))
        out.append(s)
    return out


def CreateDSAndJSON(path_to_csv: str, path_to_json: str) -> Schedule:
    # Get info.
    info = ParseCSV(path_to_csv)
    # Name it and do further parsing.
    days = info[Days.key]
    times = info[Time.key]

    rooms = info[Rooms.key]
    cap = info[RoomCapacity.key]
    CheckIntList(cap, lambda x: 'Room ' + rooms[x] + ' has an incorrect capacity.')

    ins = info[Instructors.key]
    # bad_days = info[BadDays.key]
    # bad_slots = info[BadSlots.key]

    groups = info[Groups.key]
    stud_n = info[StudentsN.key]
    CheckIntList(stud_n, lambda x: 'Group ' + groups[x] + ' has an incorrect number of students.')

    grades = info[Grades.key]
    gradegrp = ParseGroups(info[GradeGroups.key], groups,
                           lambda x: 'Grade ' + grades[x] + ' has no groups.',
                           lambda x, y: 'Grade ' + grades[x] + ' has a nonexistent group ' + y + '.')

    course = info[Course.key]
    typ = info[LessonType.key]
    CheckPresenceInList(typ, LessonTypes, lambda x: 'Course ' + course[x] + ' has an incorrect lesson type ' +
                                                    typ[x] + '.')
    whom = ParseGroups(info[GradeOrGroups.key], groups + grades,
                           lambda x: 'Course ' + course[x] + ' has no groups or grade.',
                           lambda x, y: 'Course ' + course[x] + ' has a nonexistent group or grade ' + y + '.')
    who = info[Instructor.key]
    CheckPresenceInList(who, ins, lambda x: 'Course ' + course[x] + ' has a nonexistent instructor ' + who[x] + '.')
    week_n = info[LessonsN.key]
    CheckIntList(week_n, lambda x: 'Course ' + course[x] + ' has an incorrect number of lessons.')
    week_n = [int(n) for n in week_n]
    # Init table
    gradesdict = dict()
    for i in range(len(grades)):
        gradesdict[grades[i]] = gradegrp[i]
    table = Schedule(days, times, gradesdict, list(set(course)), ins, rooms)
    CheckPresenceInList(groups, table.allGroups, lambda x: 'Group ' + groups[x] + ' has not a grade.')
    # End of parsing.
    # Convert received data into JSON.
    out = []
    # Build lessons.
    temp = []
    for i in range(len(course)):
        fp = '[' + wiq(course[i]) + ',' + wiq(typ[i]) + ','
        lp = ',' + wiq(who[i]) + ']'
        r = range(week_n[i])
        for g in whom[i]:
            s = fp + wiq(g) + lp
            for _ in r:
                temp.append(s)
    out.append(mjsonk('lessons', temp))
    # Build days.
    out.append(BuildOneValueKey('days', days))
    # Build times.
    out.append(BuildOneValueKey('time_slots', times))
    # Build rooms.
    out.append(BuildTwoValueKey('auditoriums', rooms, cap))
    # Add grades to group list.
    for i in range(len(grades)):
        p = 0
        for g in gradegrp[i]:
            j = groups.index(g)
            p += int(stud_n[j])
        groups.append(grades[i])
        stud_n.append(str(p))
    # Build groups.
    out.append(BuildTwoValueKey('student_groups', groups, stud_n))
    # Write JSON.
    with open(path_to_json, 'w', encoding='utf-8') as f:
        f.write('{' + ','.join(out) + '}')
    return table


# table = CreateDSAndJSON('SampleData.csv', 'InputJSON.json')
# table.addDataFromJSON('OutputJSON.json')
# for s in table.slots:
#     print(s)
