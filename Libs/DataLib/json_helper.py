import json
from Libs.OSLib.os_helper import file_create
import os


class JsonManager:
    """
    Json Manager
    """
    def __init__(self, filepath: type(os.path)):
        self._filepath = filepath

        file_create(self._filepath)

    def import_data(self):
        """
        Attempts to import JSON data from the filepath.
        If file does not exist, it creates a file but returns an empty list.
        :return: JSON data list
        """
        try:
            with open(self._filepath) as read_file:
                data_list = json.load(read_file)
                read_file.close()
                return data_list
        except FileNotFoundError:
            self.__create_file()
            return []
        except json.decoder.JSONDecodeError:
            return []

    def export_data(self, data_list: list):
        """
        Attempts to export JSON data to the filepath.
        If file does not exist, it creates a file and dumps the data to it.
        :param data_list: list of data to export to file.
        :return: None
        """
        indent = 4
        try:
            with open(self._filepath, 'w') as write_file:
                json.dump(data_list, write_file, indent=indent)
                write_file.close()
        except FileNotFoundError:
            self.__create_file()
            json.dump(data_list, write_file, indent=indent)

    def __create_file(self):
        """
        Creates a file in the filesystem of the filepath.
        :return: None
        """
        f = open(self._filepath, 'a')


if __name__ == '__main__':
    user_list = [
        {
            'name': 'Natalie',
            'make': 'Volkswagen',
            'model': 'Jetta',
            'license': 'fdsa',
            'email': 'caseyray.lewis@gmail.com',
        }
    ]

    json_test = JsonManager('test.json')

    # TEST EXPORT
    # json_test.export_data(user_list)

    # TEST IMPORT
    # data_list = json_test.import_data()
    # for data in data_list:
    #     for key, value in data.items():
    #         print(key, value)

    # TEST FILE EXISTS
    file_exists = file_exists('test.txt')
    print(file_exists)

