import unittest

from Libs.OSLib.chromedriver_helper import *


class TestChromedriver(unittest.TestCase):
    root_dir = os.getcwd()
    chromedriver_dir = os.path.join(root_dir, 'chromedriver')

    @classmethod
    def setUpClass(cls):
        # CREATE CHROMEDRIVER DIRECTORY
        dir_create(cls.chromedriver_dir)

    @classmethod
    def tearDownClass(cls):
        # DELETE CHROMEDRIVER DIRECTORY
        dir_remove(cls.chromedriver_dir)
        return

    def test_get_chrome_version(self):
        chrome_version = get_chrome_version()
        self.assertNotEqual(chrome_version, None)

    def test_download_chrome_driver(self):
        download_chrome_driver(self.chromedriver_dir)
        chrome_driver_exe = os.path.join(self.chromedriver_dir, 'chromedriver.exe')
        if not os.path.exists(chrome_driver_exe):
            self.fail()


if __name__ == '__main__':
    unittest.main()
