from enum import Enum


# @todo in future - use configs through special config module


class ExchangeFormat(Enum):
    CSV = 1
    DB = 2
    JSON = 3


config = {
    'size_of_population': 5,
    'schedule_mutation_rate': 0.1,
    'lesson_mutation_rate': 0.1,
    'good_error': 0,
    'penalty': 10,
    'class_change_probability': 0.3,
    'exchange_format': ExchangeFormat.CSV,

    'number_of_auditoriums': 5,
    'number_of_timeslots': 5,
    'number_of_days': 5,

    'import_csv_path': 'csv/',
    'import_json_path': 'json/schedule_data.json',
    'export_csv_path': 'csv/schedule.csv',
    'export_json_path': 'json/schedule.json'
}


def set_run_info(**params):
    """ Set configuration information. """
    for param in params:
        default = config[param]
        config[param] = params.get(param, default)
