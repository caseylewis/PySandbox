import unittest
from Libs.OSLib.chromedriver_helper import *
import getpass


class TestChromedriver(unittest.TestCase):
    root_dir = os.getcwd()
    chromedriver_dir = os.path.join(root_dir, 'chromedriver')

    @classmethod
    def setUpClass(cls):
        # CREATE CHROMEDRIVER DIRECTORY
        if not os.path.exists(cls.chromedriver_dir):
            os.umask(0)
            os.mkdir(cls.chromedriver_dir, mode=777)
            os.chmod(cls.chromedriver_dir, 744)
            # dir_create(cls.chromedriver_dir)

    @classmethod
    def tearDownClass(cls):
        # DELETE CHROMEDRIVER DIRECTORY
        # shutil.rmtree(cls.chromedriver_dir)
        return

    def test_get_chrome_version(self):
        self.assertNotEqual(get_chrome_version(), None)

    def test_download_chrome_driver(self):
        download_chrome_driver(self.chromedriver_dir)
        if not os.path.exists(os.path.join(self.chromedriver_dir, 'chromedriver.exe')):
            self.fail()


if __name__ == '__main__':
    unittest.main()
