import os
import unittest
from Libs.DataLib.json_helper import *
from Libs.OSLib.os_helper import *


# TEST LIST
INSERT_COUNT = 5
test_json_list = []
for x in range(INSERT_COUNT):
    data_dict = {
        str(0): int(x),
    }


class TestJsonHelper(unittest.TestCase):
    test_json = None
    root_dir = os.getcwd()
    test_json_path = os.path.join(root_dir, 'test.json')

    @classmethod
    def setUpClass(cls):
        cls.test_json = JsonManager(cls.test_json_path)
        cls.test_json.export_data(test_json_list)

    @classmethod
    def tearDownClass(cls) -> None:
        file_delete(cls.test_json_path)

    def test_export_data(self):
        test_json_list.append({str(0): int(INSERT_COUNT+1)})
        self.test_json.export_data(test_json_list)
        import_data = self.test_json.import_data()
        for x, y in zip(import_data, test_json_list):
            self.assertEqual(x, y)

    def test_import_data(self):
        import_data = self.test_json.import_data()
        for x, y in zip(import_data, test_json_list):
            self.assertEqual(x, y)


if __name__ == '__main__':
    unittest.main()
