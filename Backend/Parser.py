delimiter = ','


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
Slots = Row('slots')

LectureAuds = Row('lecauds', skip=1)
TutorialAuds = Row('tutauds')
LabAuds = Row('labauds')

Instructors = Row('teachers', skip=1)
BadDays = Row('baddays', False)
BadSlots = Row('badslots', False)

Grades = Row('spec', skip=1)
Groups = Row('groups', False)

Courses = Row('courses', skip=1)
LecturesN = Row('lecn', False)
TutorialsN = Row('tutn', False)
LabsN = Row('labn', False)
LectureIns = Row('lecins', False)
TutorialIns = Row('tutins', False)
LabIns = Row('labins', False)
CourseGrade = Row('cg', False)


def parse_line(line: str) -> list:
    temp = line.strip().split(delimiter)[1:]
    i = len(temp) - 1
    while temp[i] == '':
        i -= 1
    return temp[:i + 1]


def parse_line_with_bound(line: str, l: int) -> list:
    return line.strip().split(delimiter)[1:l + 1]


def parse(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        inp = f.readlines()
    info = dict()
    L = 0
    for r in Row.objects:
        if r.independent:
            info[r.key] = parse_line(inp[r.row])
            L = len(info[r.key])
        else:
            info[r.key] = parse_line_with_bound(inp[r.row], L)
        # print(r.key, '-', len(info[r.key]))
    return info


# print(parse('Sample Data.csv'))
