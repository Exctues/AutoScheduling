from Backend.Common import ListToStr, nl
from Backend import Parser

subdelimeter = '; '


# Mistakes during parsing.
class ParseError(Exception):
    pass


# Mistakes in input file.
class MalformedFile(Exception):
    pass


class Instructor:
    instructors = []

    def __init__(self, name: str, days: list, bad_days: str, slots: list, bad_slots: str):
        self.name = name
        # Init days.
        bad_days = bad_days.split(subdelimeter)
        for d in bad_days:
            if d != '' and not (d in days):
                raise MalformedFile('Instructor ' + name + ' has an unknown day ' + d + ' in busy days!')
        self.days = [days[i] for i in range(len(days)) if not (days[i] in bad_days)]
        # Init time slots.
        bad_slots = bad_slots.split(subdelimeter)
        for d in bad_slots:
            if d != '' and not (d in slots):
                raise MalformedFile('Instructor ' + name + ' has an unknown time slot ' + d + ' in busy slots!')
        self.slots = [slots[i] for i in range(len(slots)) if not (slots[i] in bad_slots)]

        Instructor.instructors.append(self)
        self.classes = []

    def __str__(self):
        return self.name

    def getAllInfo(self) -> str:
        return self.name + nl + \
               'Acceptable days: ' + ListToStr(self.days) + nl + \
               'Acceptable time slots: ' + ListToStr(self.slots) + nl

    @staticmethod
    def getInstructorByName(name: str):
        for i in Instructor.instructors:
            if i.name == name:
                return i
        return None

    def addClasses(self, classes):
        self.classes.append(classes)


class Grade:
    grades = []

    def __init__(self, name: str, groups: str):
        self.name = name
        self.groups = groups.split(subdelimeter)
        self.courses = []
        Grade.grades.append(self)

    def __str__(self):
        return '- ' + self.name + ' -' + nl + \
               'Groups: ' + ListToStr(self.groups) + nl

    @staticmethod
    def getGradeByName(name: str):
        for g in Grade.grades:
            if g.name == name:
                return g
        return None

    def addCourse(self, course):
        self.courses.append(course)


class ClassesInfo:
    Lecture = 'Lectures'
    Tutorial = 'Tutorials'
    Lab = 'Labs'

    @staticmethod
    def getClasses(typ: str, number: str, ins_names: str, auds: list):
        try:
            number = int(number)
        except ValueError:
            raise MalformedFile('Classes information contains an invalid number of classes!')
        if number > 0:
            return ClassesInfo(typ, number, ins_names, auds)
        return None

    def __init__(self, typ: str, number: int, ins_names: str, auds: list):
        self.typ = typ
        self.number = number

        self.instructors = []
        ins_names = ins_names.split(subdelimeter)
        for name in ins_names:
            teach = Instructor.getInstructorByName(name)
            if teach is None:
                raise MalformedFile('An unknown instructor conducts classes!')
            teach.addClasses(self)
            self.instructors.append(teach)

        self.auditoriums = auds
        self.course = None

    def setCourse(self, course):
        if self.course is None:
            self.course = course
        else:
            raise ParseError('Course ' + course.name + ' tries to re-set the course of a ClassesInfo instance!')

    def __str__(self):
        if self.number == 1:
            num_classes = '1 class per week.'
        else:
            num_classes = str(self.number) + ' classes per week.'
        # if len(self.instructors) == 1:
        #     h = 'Instructor: '
        # else:
        #     h = 'Instructors: '
        return self.typ + nl + \
               num_classes + nl + \
               'Instructors: ' + ListToStr(self.instructors) + nl


class Course:
    def __init__(self, name: str, classes: list, grade_name: str):
        self.name = name
        self.classes = classes
        for c in classes:
            c.setCourse(self)

        g = Grade.getGradeByName(grade_name)
        if g is None:
            raise MalformedFile('An unknown grade has a course!')
        g.addCourse(self)
        self.grade = g

    def __str__(self):
        return '- ' + self.name + ' -' + nl + \
               'Grade: ' + self.grade.name + nl + \
               ListToStr(self.classes, nl, '')


class ScheduleData:
    def __init__(self, days: list, slots: list, lec_auds: list, tut_auds: list, lab_auds: list,
                 ins: list, grades: list, courses: list):
        self.days = days
        self.slots = slots
        self.auds = list(set(lec_auds + tut_auds + lab_auds))
        self.auds.sort()
        self.ins = ins
        self.grades = grades
        self.courses = courses

    def __str__(self):
        return 'Days: ' + ListToStr(self.days) + nl + \
               'Time slots: ' + ListToStr(self.slots) + nl + \
               'Auditoriums: ' + ListToStr(self.auds) + nl + nl + \
               '-- Instructors --' + nl + \
               ListToStr(self.ins, nl, '', Instructor.getAllInfo) + nl + \
               '-- Grades --' + nl + \
               ListToStr(self.grades, nl, '') + nl + \
               '-- Courses --' + nl + \
               ListToStr(self.courses, nl, '')


def getScheduleData(file_path: str) -> ScheduleData:
    # Get info.
    info = Parser.parse(file_path)
    # Name it.
    days = info[Parser.Days.key]
    slots = info[Parser.Slots.key]

    lec_auds = info[Parser.LectureAuds.key]
    tut_auds = info[Parser.TutorialAuds.key]
    lab_auds = info[Parser.LabAuds.key]

    ins = info[Parser.Instructors.key]
    bad_days = info[Parser.BadDays.key]
    bad_slots = info[Parser.BadSlots.key]

    grades = info[Parser.Grades.key]
    groups = info[Parser.Groups.key]

    courses = info[Parser.Courses.key]
    lec_n = info[Parser.LecturesN.key]
    tut_n = info[Parser.TutorialsN.key]
    lab_n = info[Parser.LabsN.key]
    lec_ins = info[Parser.LectureIns.key]
    tut_ins = info[Parser.TutorialIns.key]
    lab_ins = info[Parser.LabIns.key]
    specs = info[Parser.CourseGrade.key]
    # Init instructors.
    for i in range(len(ins)):
        Instructor(ins[i], days, bad_days[i], slots, bad_slots[i])
    # Init grades.
    for i in range(len(grades)):
        Grade(grades[i], groups[i])

    # Init courses.
    R = range(len(courses))
    # Init classes.
    Classes = []
    for i in R:
        lec = ClassesInfo.getClasses(ClassesInfo.Lecture, lec_n[i], lec_ins[i], lec_auds)
        tut = ClassesInfo.getClasses(ClassesInfo.Tutorial, tut_n[i], tut_ins[i], tut_auds)
        lab = ClassesInfo.getClasses(ClassesInfo.Lab, lab_n[i], lab_ins[i], lab_auds)
        li = [lec, tut, lab]
        Classes.append([c for c in li if not (c is None)])
    Courses = []
    for i in R:
        Courses.append(Course(courses[i], Classes[i], specs[i]))

    return ScheduleData(days, slots, lec_auds, tut_auds, lab_auds, Instructor.instructors, Grade.grades, Courses)


# print(getScheduleData('Backend/Sample Data.csv'))
