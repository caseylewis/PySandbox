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
            register_2_park(
                chromedriver_path=self.chromedriver_dir,
                make='Toyota',
                model='Avalon',
                license_plate='CZX0399',
                email='caseyray.lewis@gmail.com',
                apartment_number='621',
            )
        except Exception as e:
            self.fail()

    def test_RegisterInfo(self):
        test_reg_info = RegisterInfo()

        # TEST DEFAULTS
        self.assertEqual(test_reg_info.make, RegisterDefaults.MAKE)
        self.assertEqual(test_reg_info.model, RegisterDefaults.MODEL)
        self.assertEqual(test_reg_info.license_plate, RegisterDefaults.LICENSE_PLATE)
        self.assertEqual(test_reg_info.email, RegisterDefaults.EMAIL)
        self.assertEqual(test_reg_info.chromedriver_path, RegisterDefaults.CHROMEDRIVER_PATH)

        # TEST UPDATED VALUES
        test_reg_info.make = 'new_make'
        test_reg_info.model = 'new_model'
        test_reg_info.license_plate = 'new_license'
        test_reg_info.email = 'new_email'
        test_reg_info.chromedriver_path = 'new_chromedriver'

        self.assertEqual(test_reg_info.make, 'new_make')
        self.assertEqual(test_reg_info.model, 'new_model')
        self.assertEqual(test_reg_info.license_plate, 'new_license')
        self.assertEqual(test_reg_info.email, 'new_email')
        self.assertEqual(test_reg_info.chromedriver_path, 'new_chromedriver')


if __name__ == '__main__':
    unittest.main()
