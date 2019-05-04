## -*- coding: utf-8 -*-

import csv
import json
import pandas as pd
from schedule.config import config, ExchangeFormat


class Exchanger:

    @staticmethod
    def import_data(exchange_format: ExchangeFormat) -> dict:
        """ Import data from CSV/JSON """
        data = {'lessons': [], 'days': [], 'time_slots': [], 'auditoriums': [], 'student_groups': []}

        if exchange_format is ExchangeFormat.CSV:
            for filename in ['lessons', 'days', 'time_slots', 'auditoriums', 'student_groups']:
                csv_path = f"{config['import_csv_path']}{filename}.csv"
                with open(csv_path, "r", encoding="utf-8") as input_file:
                    reader = csv.reader(input_file)
                    for row in reader:
                        data[filename].append(row)

        if exchange_format is ExchangeFormat.JSON:
            with open(config['import_json_path'], "r", encoding="utf-8") as input_file:
                data = json.load(input_file)

        return data

    @staticmethod
    def export_data(data: list, exchange_format: ExchangeFormat) -> None:
        """ Export data to CSV/JSON """
        if exchange_format is ExchangeFormat.CSV:
            with open(config['export_csv_path'], "w", encoding="utf-8") as output_file:
                writer = csv.writer(output_file)
                for row in data:
                    writer.writerow(row.values())

            Exchanger.remove_new_lines_from_csv(config['export_csv_path'])

        if exchange_format is ExchangeFormat.JSON:
            with open(config['export_json_path'], "w", encoding="utf-8") as output_file:
                json.dump(data, output_file, ensure_ascii=False)

    @staticmethod
    def csv_to_json():
        """ Transform input CSV to JSON """
        data = {'lessons': [], 'days': [], 'time_slots': [], 'auditoriums': [], 'student_groups': []}

        for filename in ['lessons', 'days', 'time_slots', 'auditoriums', 'student_groups']:
            csv_path = f"{config['import_csv_path']}{filename}.csv"
            json_path = config['import_json_path']
            with open(csv_path, "r", encoding="utf-8") as input_file:
                reader = csv.reader(input_file)
                for row in reader:
                    data[filename].append(row)
            with open(json_path, "w", encoding="utf-8") as output_file:
                json.dump(data, output_file, ensure_ascii=False)

    @staticmethod
    def json_to_csv(json_path, csv_path):
        data = []

        with open(json_path, "r", encoding="utf-8") as input_file:
            data = json.load(input_file)
        with open(csv_path, "w", encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            for row in data:
                writer.writerow(row.values())
        Exchanger.remove_new_lines_from_csv(csv_path)

    @staticmethod
    def remove_new_lines_from_csv(csv_path):
        with open(csv_path, "r+", encoding="utf-8") as file:
            rows = file.readlines()
            file.truncate(0)
            for row in rows:
                if len(row) == 1 and row[0] == '\n':
                    continue
                file.write(row)

    @staticmethod
    def json_to_cfg(path_to_json, path_to_cfg):
        print(path_to_cfg)
        test_data2 = json.load(open(path_to_json))
        #print(path_to_json)
        days = [i for j in test_data2['days'] for i in j]
        time_slots = [i for j in test_data2['time_slots'] for i in j]

        auditoriums = [(i, int(j)) for i, j in test_data2['auditoriums']]
        student_groups = {i: int(j) for i, j in sorted(test_data2['student_groups'])}

        lessons = pd.DataFrame(test_data2['lessons'], columns=['course', 'type', 'group', 'lector'])
        small_groups = [i for i in student_groups if not have_subgroup(i, student_groups)]
        profs = lessons.lector.unique()
        courses = lessons.course.unique()

        profs_str = [dict_to_str_config({'id': i, 'name': prof}, 'prof') for i, prof in enumerate(profs, 1)]
        profs_str = '\n\n'.join(profs_str)
        courses_str = [dict_to_str_config({'id': i, 'name': prof}, 'course') for i, prof in enumerate(courses, 1)]
        courses_str = '\n\n'.join(courses_str)
        rooms_str = [{'name': aud, 'lab': is_lab(aud), 'size': cap} for aud, cap in auditoriums]
        rooms_str = '\n\n'.join([dict_to_str_config(x, 'room') for x in rooms_str])
        group_str = [{'id': i, 'name': g, 'size': student_groups[g]} for i, g in enumerate(small_groups, 1)]
        group_str = '\n\n'.join([dict_to_str_config(x, 'group') for x in group_str])
        #print(lessons)
        #print(small_groups)
        lessons_str = df_to_dict(lessons, small_groups)

        print(path_to_cfg)

        with open(path_to_cfg, 'w') as f:
            print(courses_str)
            print(rooms_str)
            print(group_str)
            print(lessons_str)
            l = [profs_str, courses_str, rooms_str, group_str, lessons_str]
            print('\n\n'.join(l))
            f.write('\n\n'.join(l))


def have_subgroup(group, groups):
    for g in groups:
        if group != g and g.startswith(group):
            return True
    return False


def dict_to_str_config(d, open_tag):
    st = f'#{open_tag}\n'
    for key, value in d.items():
        if isinstance(value, list):
            for v in value:
                st += f'\t{key} = {v}\n'
        else:
            st += f'\t{key} = {value}\n'
    st += '#end'
    return st


def is_lab(aud):
    return 'false' if aud in ['105', '106', '107', '108'] else 'true'


def df_to_dict(lessons, groups):
    profs_dict = {prof: i for i, prof in enumerate(lessons.lector.unique(), 1)}
    courses_dict = {cours: i for i, cours in enumerate(lessons.course.unique(), 1)}
    groups_dict = {group: i for i, group in enumerate(groups, 1)}
    classes_str = []
    lessons = lessons.values
    for course, ltype, group, lector in lessons:
        d = {'professor': profs_dict[lector], 'course': courses_dict[course], 'duration': 1}
        if group in groups:
            d['group'] = groups_dict[group]
            d['lab'] = 'true'
        else:
            d['group'] = [groups_dict[g] for g in groups if g.startswith(group)]
            if ltype == 'Tutorial':
                d['tutorial'] = 'true'
        classes_str.append(dict_to_str_config(d, 'class'))
    print(classes_str)
    return '\n\n'.join(classes_str)


