from math import ceil

from schedule.data_exchange import Exchanger
from copy import copy
from random import randint, uniform, choice

from schedule.data_process import DataProcessor
from schedule.config import config


def dmap(i, j, k=0):
    return [[k] * j for _ in range(i)]


def allocate_maps():
    map_size = 100
    map_node_size = 100
    proff_map = dmap(map_size, map_node_size)
    audit_map = dmap(map_size, map_node_size)
    group_map = dmap(map_size, map_node_size)
    return proff_map, audit_map, group_map


# Dont bother for now
proff_map, audit_map, group_map = allocate_maps()


class Lesson:
    __slots__ = ('time', 'lecture_name', 'group', 'day', 'auditorium', 'faculty')

    def __init__(self, time, lecture_name, group, day, auditorium, faculty):
        self.time = time
        self.lecture_name = lecture_name
        self.group = group
        self.day = day
        self.auditorium = auditorium
        self.faculty = faculty

    def __str__(self):
        return f'Lec_name: {self.lecture_name},Faculty: {self.faculty}, Group: {self.group}, Day: {self.day}, Time: {self.time}, Auditorium: {self.auditorium}'

    def __repr__(self):
        return f'Lesson - {id(self)} instance - {self}'


class Schedule:

    def __init__(self, lessons):
        self.lessons = lessons
        self.score = None

    def __iter__(self):
        return iter(self.lessons)

    def __len__(self):
        return len(self.lessons)

    @property
    def fitness(self):
        """Calculate fitness function on this schedule"""
        score = 0
        for lesson in self.lessons:
            key = lesson.day * 10 + lesson.time
            group_map[lesson.group][key] += 1
            proff_map[lesson.faculty][key] += 1
            audit_map[lesson.auditorium][key] += 1

        for lesson in self.lessons:
            key = lesson.day * 10 + lesson.time

            score += max(0, group_map[lesson.group][key] - 1) * config['penalty']
            score += max(0, audit_map[lesson.auditorium][key] - 1) * config['penalty']
            score += max(0, proff_map[lesson.faculty][key] - 1) * config['penalty']

            group_map[lesson.group][key] = 0
            audit_map[lesson.auditorium][key] = 0
            proff_map[lesson.faculty][key] = 0

        return score

    def mutate(self):
        """Mutate this schedule - change date time and auditorium of lesson with some probability"""
        for lesson in self.lessons:
            if uniform(0, 1) < config['schedule_mutation_rate']:
                lesson.auditorium = randint(0, config['number_of_auditoriums'])
                lesson.day = randint(0, config['number_of_days'])
                lesson.time = randint(0, config['number_of_timeslots'])

    @staticmethod
    def crossover(s1_: 'Schedule', s2_: 'Schedule') -> tuple:
        """Cross schedule self with schedule s - randomly swap some number of
            lessons between schedules and get two new individuals
        """
        s1 = copy(s1_)
        s2 = copy(s2_)
        number_of_swaps = ceil(len(s1.lessons) / 10)
        rand_lessons_s1 = [randint(0, len(s1.lessons) - 1) for _ in range(number_of_swaps)]
        rand_lessons_s2 = [randint(0, len(s2.lessons) - 1) for _ in range(number_of_swaps)]
        for r1, r2 in zip(rand_lessons_s1, rand_lessons_s2):
            l1 = s1.lessons[r1]
            l2 = s2.lessons[r2]
            l1.time, l2.time = l2.time, l1.time
            l1.day, l2.day = l2.day, l1.day
            if uniform(0, 1) < config['class_change_probability']:
                l1.auditorium, l2.auditorium = \
                    l2.auditorium, l1.auditorium
        return s1, s2

    def __str__(self):
        """Represent schedule in string format"""
        res = '\n'.join(str(lesson) for lesson in self.lessons)
        return f'\n[{res}]\n'

    def __repr__(self):
        return f'Schedule - {id(self)}  : {self}'

    def __copy__(self):
        return Schedule([copy(lesson) for lesson in self.lessons])


class Population:

    def __init__(self):
        self.individuals = []

    def __iter__(self):
        return iter(self.individuals)

    def __len__(self):
        return len(self.individuals)

    def add(self, individ: Schedule):
        self.individuals.append(individ)

    @property
    def best_individual(self) -> Schedule:
        best = None
        best_score = 0
        for schedule in self.individuals:
            s = schedule.fitness
            if s < best_score or best is None:
                best = schedule
                best_score = s
        return best

    def select_best(self) -> 'Population':
        """ Make selection process (choose n best)"""
        inds = []
        for ind, schedule in enumerate(self.individuals):
            inds.append((schedule, schedule.fitness,))
        inds.sort(key=lambda i: i[1])
        inds = inds[:config['size_of_population']]
        new_population = Population()
        for ind_best in inds:
            new_population.add(ind_best[0])
        return new_population

    def cross_and_mutate(self):
        """Cross random schedules and get new population"""
        n = len(self.individuals)
        # Crossover procedure
        new_population = Population()
        for i in range(n):
            s1 = self.individuals[randint(0, n - 1)]
            s2 = self.individuals[randint(0, n - 1)]
            ch1, ch2 = Schedule.crossover(s1, s2)
            new_population.add(ch1)
            new_population.add(ch2)
        for schedule in new_population.individuals:
            schedule.mutate()
        new_population.add(self.best_individual)
        return new_population

    def evolve(self) -> 'Population':
        """One evolution iteration"""
        pop = self.select_best()
        pop = pop.cross_and_mutate()
        return pop

    def __str__(self):
        return '\n'.join(map(str, self.individuals))


class GeneticSchedule:

    @staticmethod
    def set_run_info(number_of_auditoriums, number_of_timeslots, number_of_days):
        config['number_of_days'] = number_of_days - 1
        config['number_of_auditoriums'] = number_of_auditoriums - 1
        config['number_of_timeslots'] = number_of_timeslots - 1

    @staticmethod
    def create_initial(lessons: list) -> Population:
        """ Make initial population"""
        pop = Population()
        sch = Schedule(lessons=lessons)
        for i in range(config['size_of_population']):
            for lesson in sch.lessons:
                lesson.time = randint(0, config['number_of_timeslots'])
                lesson.day = randint(0, config['number_of_days'])
                lesson.auditorium = randint(0, config['number_of_auditoriums'])
            pop.add(copy(sch))
        return pop

    @staticmethod
    def get_initial_population(data=None, set_config=False) -> Population:
        print(data)
        """Make initial population based on data from CSV/JSON (at the moment)"""
        if data is None:
            data = Exchanger.import_data(config['exchange_format'])

        data = DataProcessor.enumerate_data(data)
        initial_population = Population()
        if set_config:
            GeneticSchedule.set_run_info(len(data['auditoriums']), len(data['time_slots']), len(data['days']))
        for i in range(config['size_of_population']):
            lessons_list = []
            for lesson in data['lessons']:
                day = choice(data['days'])
                time_slot = choice(data['time_slots'])
                auditorium = choice(data['auditoriums'])
                slot = Lesson(time_slot, (lesson[0], lesson[1]), lesson[2], day, auditorium, lesson[3])
                lessons_list.append(slot)
            initial_population.add(individ=Schedule(lessons_list))

        return initial_population

    @staticmethod
    def run(initial: Population) -> Schedule:
        """ Evolve initial population until we found a solution"""
        population = initial
        generation = 0
        while population.best_individual.fitness > config['good_error']:
            population = population.evolve()
            generation += 1
        return population.best_individual
