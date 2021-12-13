import unittest
from App_3500ParkingLogin.data_types.users import *
from App_3500ParkingLogin.data_types.parking_sessions import *
from App_3500ParkingLogin.register_2_park import *
from Libs.OSLib.os_helper import *


user = {
    User.keys.MAKE: 'Toyota',
    User.keys.MODEL: 'Avalon',
    User.keys.LICENSE_PLATE: 'CZX0399',
    User.keys.EMAIL: 'caseyray.lewis@gmail.com'
}
session = NewParkingSession('casey', user, 0, 0, 0, True)


class TestRegister2Park(unittest.TestCase):
    root_dir = os.getcwd()
    chromedriver_dir = os.path.join(root_dir, 'chromedriver')

    @classmethod
    def setUpClass(cls) -> None:
        dir_create(cls.chromedriver_dir)

    @classmethod
    def tearDownClass(cls) -> None:
        dir_remove(cls.chromedriver_dir)

    def test_register_2_park(self):
        try:
            register_2_park(chromedriver_path=self.chromedriver_dir, **user)
        except Exception as e:
            self.fail()


if __name__ == '__main__':
    unittest.main()
