import unittest
import os

from schedule.data_process import DataProcessor
from schedule.ga import Schedule, Lesson, GeneticSchedule
from schedule.config import set_run_info, config
from schedule.data_exchange import Exchanger, ExchangeFormat


class TestInvididual(unittest.TestCase):

    def test_fitness1(self):
        # No intersections
        data = [Lesson(time=1, lecture_name=2, group=3, day=2, auditorium=4, faculty=1),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=6, faculty=2),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=5, faculty=3),
                ]

        s = Schedule(lessons=data).fitness
        self.assertEqual(s, 0)

    def test_fitness2(self):
        # One intersection
        data = [Lesson(time=1, lecture_name=2, group=2, day=2, auditorium=4, faculty=1),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=6, faculty=2),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=5, faculty=3),
                ]

        s = Schedule(lessons=data).fitness
        self.assertEqual(s, config['penalty'])

    def test_fitness3(self):
        # Two intersections - one extra lecture for professor & one extra
        # lecture for same group per time slot
        data = [Lesson(time=1, lecture_name=2, group=2, day=2, auditorium=4, faculty=3),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=6, faculty=2),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=5, faculty=3),
                ]

        s = Schedule(lessons=data).fitness
        self.assertEqual(s, config['penalty'] * 2)

    def test_fitness4(self):
        data = [Lesson(time=1, lecture_name=2, group=2, day=2, auditorium=4, faculty=3),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=4, faculty=2),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=5, faculty=3),
                ]

        s = Schedule(lessons=data).fitness
        self.assertEqual(s, config['penalty'] * 3)

    def test_csv_import(self):
        # Check that data imported from CSV file has correct structure
        set_run_info(import_csv_path='csv/')
        data = Exchanger.import_data(ExchangeFormat.CSV)
        self.assertGreater(len(data), 0)
        self.assertGreater(len(data['lessons']), 0)
        self.assertGreater(len(data['days']), 0)
        self.assertGreater(len(data['time_slots']), 0)
        self.assertGreater(len(data['auditoriums']), 0)
        self.assertGreater(len(data['student_groups']), 0)

    def test_json_import(self):
        # Check that data imported from JSON file has correct structure
        set_run_info(import_json_path='json/schedule_data.json')
        data = Exchanger.import_data(ExchangeFormat.JSON)
        self.assertGreater(len(data), 0)
        self.assertGreater(len(data['lessons']), 0)
        self.assertGreater(len(data['days']), 0)
        self.assertGreater(len(data['time_slots']), 0)
        self.assertGreater(len(data['auditoriums']), 0)
        self.assertGreater(len(data['student_groups']), 0)

    def test_csv_export(self):
        # Check that file with JSON data exists after export
        # ToDO validate correctness of data in output file
        set_run_info(export_json_path='json/test.json')
        data = [{'Course_name': 'DSA', 'Lesson_type': 'Lecture', 'Faculty': 'Adil', 'Group': 'BS17', 'Day': 'Monday',
                 'Time': '17:20-18:50', 'Auditorium': '103'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-01',
                 'Day': 'Wednesday', 'Time': '10:35-12:05', 'Auditorium': '106'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-02',
                 'Day': 'Wednesday', 'Time': '09:00-10:30', 'Auditorium': '108'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-03', 'Day': 'Monday',
                 'Time': '15:45-17:15', 'Auditorium': '106'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-05',
                 'Day': 'Saturday', 'Time': '17:20-18:50', 'Auditorium': '103'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-06', 'Day': 'Tuesday',
                 'Time': '17:20-18:50', 'Auditorium': '101'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-07',
                 'Day': 'Wednesday', 'Time': '17:20-18:50', 'Auditorium': '104'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-08', 'Day': 'Friday',
                 'Time': '15:45-17:15', 'Auditorium': '105'}, {'Course_name': 'Intro to AI', 'Lesson_type': 'Lecture',
                                                               'Faculty': 'Professor Professor Doctor Joseph Alexander Brown IEEE Senior Member Fallout 76 and Neural Networks Hater',
                                                               'Group': 'BS17', 'Day': 'Saturday',
                                                               'Time': '18:55-20:25', 'Auditorium': '108'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Tutorial', 'Faculty': 'Hamna', 'Group': 'BS17',
                 'Day': 'Friday', 'Time': '10:35-12:05', 'Auditorium': '102'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-01',
                 'Day': 'Wednesday', 'Time': '09:00-10:30', 'Auditorium': '105'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-02',
                 'Day': 'Tuesday', 'Time': '17:20-18:50', 'Auditorium': '105'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-03',
                 'Day': 'Saturday', 'Time': '15:45-17:15', 'Auditorium': '103'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-05',
                 'Day': 'Saturday', 'Time': '12:10-13:40', 'Auditorium': '106'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-06',
                 'Day': 'Friday', 'Time': '17:20-18:50', 'Auditorium': '108'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-07',
                 'Day': 'Wednesday', 'Time': '10:35-12:05', 'Auditorium': '105'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-08',
                 'Day': 'Thursday', 'Time': '14:10-15:40', 'Auditorium': '108'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lecture', 'Faculty': 'Gorodetskiy', 'Group': 'BS18',
                 'Day': 'Monday', 'Time': '18:55-20:25', 'Auditorium': '108'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Tutorial', 'Faculty': 'Gorodetskiy', 'Group': 'BS18',
                 'Day': 'Wednesday', 'Time': '15:45-17:15', 'Auditorium': '104'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-01',
                 'Day': 'Saturday', 'Time': '09:00-10:30', 'Auditorium': '106'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-02',
                 'Day': 'Tuesday', 'Time': '09:00-10:30', 'Auditorium': '101'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-03',
                 'Day': 'Friday', 'Time': '14:10-15:40', 'Auditorium': '104'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-04',
                 'Day': 'Tuesday', 'Time': '14:10-15:40', 'Auditorium': '106'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Rustam', 'Group': 'BS18-05',
                 'Day': 'Monday', 'Time': '18:55-20:25', 'Auditorium': '103'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Rustam', 'Group': 'BS18-06',
                 'Day': 'Friday', 'Time': '09:00-10:30', 'Auditorium': '301'},
                {'Course_name': 'DML', 'Lesson_type': 'Lecture', 'Faculty': 'Nikolay', 'Group': 'BS18', 'Day': 'Friday',
                 'Time': '09:00-10:30', 'Auditorium': '108'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-01', 'Day': 'Friday',
                 'Time': '09:00-10:30', 'Auditorium': '105'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-02', 'Day': 'Saturday',
                 'Time': '18:55-20:25', 'Auditorium': '109'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-03', 'Day': 'Tuesday',
                 'Time': '14:10-15:40', 'Auditorium': '301'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-04', 'Day': 'Monday',
                 'Time': '10:35-12:05', 'Auditorium': '107'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-05', 'Day': 'Monday',
                 'Time': '12:10-13:40', 'Auditorium': '105'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-06', 'Day': 'Monday',
                 'Time': '15:45-17:15', 'Auditorium': '107'},
                {'Course_name': 'DSP', 'Lesson_type': 'Lecture', 'Faculty': 'Nikolay', 'Group': 'B16-DS',
                 'Day': 'Saturday', 'Time': '10:35-12:05', 'Auditorium': '302'},
                {'Course_name': 'Information Retrieval', 'Lesson_type': 'Lecture', 'Faculty': 'Joo Lee',
                 'Group': 'B16-DS-01', 'Day': 'Monday', 'Time': '17:20-18:50', 'Auditorium': '302'}]
        Exchanger.export_data(data, ExchangeFormat.CSV)
        os.stat(config['export_csv_path'])

    def test_json_export(self):
        # Check that file with JSON data exists after export
        # ToDO validate correctness of data in output file
        set_run_info(export_json_path='json/test.json')
        data = [{'Course_name': 'DSA', 'Lesson_type': 'Lecture', 'Faculty': 'Adil', 'Group': 'BS17', 'Day': 'Monday',
                 'Time': '17:20-18:50', 'Auditorium': '103'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-01',
                 'Day': 'Wednesday', 'Time': '10:35-12:05', 'Auditorium': '106'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-02',
                 'Day': 'Wednesday', 'Time': '09:00-10:30', 'Auditorium': '108'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-03', 'Day': 'Monday',
                 'Time': '15:45-17:15', 'Auditorium': '106'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-05',
                 'Day': 'Saturday', 'Time': '17:20-18:50', 'Auditorium': '103'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-06', 'Day': 'Tuesday',
                 'Time': '17:20-18:50', 'Auditorium': '101'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-07',
                 'Day': 'Wednesday', 'Time': '17:20-18:50', 'Auditorium': '104'},
                {'Course_name': 'DSA', 'Lesson_type': 'Lab', 'Faculty': 'Ruzilya', 'Group': 'BS17-08', 'Day': 'Friday',
                 'Time': '15:45-17:15', 'Auditorium': '105'}, {'Course_name': 'Intro to AI', 'Lesson_type': 'Lecture',
                                                               'Faculty': 'Professor Professor Doctor Joseph Alexander Brown IEEE Senior Member Fallout 76 and Neural Networks Hater',
                                                               'Group': 'BS17', 'Day': 'Saturday',
                                                               'Time': '18:55-20:25', 'Auditorium': '108'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Tutorial', 'Faculty': 'Hamna', 'Group': 'BS17',
                 'Day': 'Friday', 'Time': '10:35-12:05', 'Auditorium': '102'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-01',
                 'Day': 'Wednesday', 'Time': '09:00-10:30', 'Auditorium': '105'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-02',
                 'Day': 'Tuesday', 'Time': '17:20-18:50', 'Auditorium': '105'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-03',
                 'Day': 'Saturday', 'Time': '15:45-17:15', 'Auditorium': '103'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Hamna', 'Group': 'BS17-05',
                 'Day': 'Saturday', 'Time': '12:10-13:40', 'Auditorium': '106'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-06',
                 'Day': 'Friday', 'Time': '17:20-18:50', 'Auditorium': '108'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-07',
                 'Day': 'Wednesday', 'Time': '10:35-12:05', 'Auditorium': '105'},
                {'Course_name': 'Intro to AI', 'Lesson_type': 'Lab', 'Faculty': 'Nikita', 'Group': 'BS17-08',
                 'Day': 'Thursday', 'Time': '14:10-15:40', 'Auditorium': '108'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lecture', 'Faculty': 'Gorodetskiy', 'Group': 'BS18',
                 'Day': 'Monday', 'Time': '18:55-20:25', 'Auditorium': '108'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Tutorial', 'Faculty': 'Gorodetskiy', 'Group': 'BS18',
                 'Day': 'Wednesday', 'Time': '15:45-17:15', 'Auditorium': '104'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-01',
                 'Day': 'Saturday', 'Time': '09:00-10:30', 'Auditorium': '106'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-02',
                 'Day': 'Tuesday', 'Time': '09:00-10:30', 'Auditorium': '101'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-03',
                 'Day': 'Friday', 'Time': '14:10-15:40', 'Auditorium': '104'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Oleg', 'Group': 'BS18-04',
                 'Day': 'Tuesday', 'Time': '14:10-15:40', 'Auditorium': '106'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Rustam', 'Group': 'BS18-05',
                 'Day': 'Monday', 'Time': '18:55-20:25', 'Auditorium': '103'},
                {'Course_name': 'Calculus', 'Lesson_type': 'Lab', 'Faculty': 'Rustam', 'Group': 'BS18-06',
                 'Day': 'Friday', 'Time': '09:00-10:30', 'Auditorium': '301'},
                {'Course_name': 'DML', 'Lesson_type': 'Lecture', 'Faculty': 'Nikolay', 'Group': 'BS18', 'Day': 'Friday',
                 'Time': '09:00-10:30', 'Auditorium': '108'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-01', 'Day': 'Friday',
                 'Time': '09:00-10:30', 'Auditorium': '105'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-02', 'Day': 'Saturday',
                 'Time': '18:55-20:25', 'Auditorium': '109'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-03', 'Day': 'Tuesday',
                 'Time': '14:10-15:40', 'Auditorium': '301'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-04', 'Day': 'Monday',
                 'Time': '10:35-12:05', 'Auditorium': '107'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-05', 'Day': 'Monday',
                 'Time': '12:10-13:40', 'Auditorium': '105'},
                {'Course_name': 'DML', 'Lesson_type': 'Lab', 'Faculty': 'Alexey', 'Group': 'BS18-06', 'Day': 'Monday',
                 'Time': '15:45-17:15', 'Auditorium': '107'},
                {'Course_name': 'DSP', 'Lesson_type': 'Lecture', 'Faculty': 'Nikolay', 'Group': 'B16-DS',
                 'Day': 'Saturday', 'Time': '10:35-12:05', 'Auditorium': '302'},
                {'Course_name': 'Information Retrieval', 'Lesson_type': 'Lecture', 'Faculty': 'Joo Lee',
                 'Group': 'B16-DS-01', 'Day': 'Monday', 'Time': '17:20-18:50', 'Auditorium': '302'}]
        Exchanger.export_data(data, ExchangeFormat.JSON)
        os.stat(config['export_json_path'])

    def test_csv_to_json(self):
        # Check that file with JSON data exists after transformation
        set_run_info(import_json_path='json/imported_schedule_data.json')
        Exchanger.csv_to_json()
        os.stat(config['import_json_path'])

    def test_initial_population1(self):
        # Test that created population has given size
        set_run_info(size_of_population=10, exchange_format=ExchangeFormat.CSV)
        population = GeneticSchedule.get_initial_population()
        self.assertEqual(10, len(population))

    def test_denumerate_schedule(self):
        # Test that data denumeration do not crash
        GeneticSchedule.set_run_info(number_of_auditoriums=23, number_of_timeslots=7, number_of_days=6)
        pop = GeneticSchedule.get_initial_population()
        best = GeneticSchedule.run(pop)
        schedule = DataProcessor.denumerate_data(best)
        self.assertEqual(len(best), len(schedule))

    def test_system1(self):
        GeneticSchedule.set_run_info(number_of_auditoriums=3, number_of_timeslots=3, number_of_days=1)
        data = [Lesson(time=1, lecture_name=2, group=2, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=3),
                ]
        pop = GeneticSchedule.create_initial(lessons=data)
        best = GeneticSchedule.run(pop)
        self.assertEqual(best.fitness, 0)
        self.assert_no_intersections(best)

    def test_system2(self):
        GeneticSchedule.set_run_info(number_of_auditoriums=3, number_of_timeslots=3, number_of_days=5)
        data = [Lesson(time=1, lecture_name=2, group=2, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=4, group=3, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=4, group=4, day=2, auditorium=1, faculty=4),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=5),
                Lesson(time=1, lecture_name=4, group=5, day=2, auditorium=1, faculty=5),
                Lesson(time=1, lecture_name=4, group=6, day=2, auditorium=1, faculty=6),
                Lesson(time=1, lecture_name=4, group=3, day=2, auditorium=1, faculty=7),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=8),

                ]
        pop = GeneticSchedule.create_initial(lessons=data)
        best = GeneticSchedule.run(pop)
        self.assertEqual(best.fitness, 0)
        self.assert_no_intersections(best)

    def test_system3(self):
        GeneticSchedule.set_run_info(number_of_auditoriums=1, number_of_timeslots=6, number_of_days=2)
        data = [Lesson(time=1, lecture_name=2, group=2, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=1, faculty=2),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=4, group=3, day=2, auditorium=1, faculty=1),
                Lesson(time=1, lecture_name=4, group=4, day=2, auditorium=1, faculty=4),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=5),
                Lesson(time=1, lecture_name=4, group=5, day=2, auditorium=1, faculty=5),
                Lesson(time=1, lecture_name=4, group=6, day=2, auditorium=1, faculty=6),
                Lesson(time=1, lecture_name=4, group=3, day=2, auditorium=1, faculty=7),
                Lesson(time=1, lecture_name=4, group=1, day=2, auditorium=1, faculty=8),
                Lesson(time=1, lecture_name=2, group=2, day=2, auditorium=1, faculty=3),
                Lesson(time=1, lecture_name=3, group=2, day=2, auditorium=1, faculty=2),
                ]
        pop = GeneticSchedule.create_initial(lessons=data)
        best = GeneticSchedule.run(pop)
        self.assertEqual(best.fitness, 0)
        self.assert_no_intersections(best)

    def test_system4(self):
        GeneticSchedule.set_run_info(number_of_auditoriums=23, number_of_timeslots=7, number_of_days=6)
        pop = GeneticSchedule.get_initial_population()
        best = GeneticSchedule.run(pop)
        self.assertEqual(best.fitness, 0)

    def assert_no_intersections(self, best):
        for l1 in best.lessons:
            for l2 in best.lessons:
                if l1 != l2 and l1.time == l2.time and l1.day == l2.day:
                    self.assertTrue(l1.auditorium != l2.auditorium)
                    self.assertTrue(l1.group != l2.group)
                    self.assertTrue(l1.faculty != l2.faculty)

    def test_dict_import2(self):
        pop = GeneticSchedule.get_initial_population({
            "lessons": [["DSA", "Lecture", "BS17", "Adil"], ["DML", "Lecture", "BS17", "Nikolay"]],
            "days": [["Monday"], ["Tuesday"], ["Wednesday"]],
            "time_slots": [["09:00-10:30"], ["10:35-12:05"], ["12:10-13:40"], ["14:10-15:40"]],
            "auditoriums": [["101", "20"], ["102", "20"], ["103", "20"], ["104", "20"], ["105", "150"], ["106", "100"]],
            "student_groups": [["BS18", "150"], ["BS17", "150"], ["B16", "60"], ["B16-DS", "25"]]
        }
        )

        sch = GeneticSchedule.run(pop)
        self.assert_no_intersections(sch)


if __name__ == '__main__':
    unittest.main()
