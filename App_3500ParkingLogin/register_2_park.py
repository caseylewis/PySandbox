from selenium import webdriver
import os
from selenium.common.exceptions import WebDriverException
from Libs.OSLib.chromedriver_helper import download_chrome_driver, CHROMEDRIVER_EXE_NAME
from Libs.OSLib.os_helper import *


apt_number = "1223"
email_address = 'caseyray.lewis@gmail.com'


class RegisterKeys:
    MAKE = 'make'
    MODEL = 'model'
    LICENSE_PLATE = 'license_plate'
    EMAIL = 'email',
    CHROMEDRIVER_PATH = 'chromedriver_path'
    APARTMENT_NUMBER = 'apartment_number'

    all_keys = [
        MAKE,
        MODEL,
        LICENSE_PLATE,
        CHROMEDRIVER_PATH,
    ]


class RegisterDefaults:
    MAKE = 'DEFAULT_MAKE'
    MODEL = 'DEFAULT_MODEL'
    LICENSE_PLATE = 'DEFAULT_LICENSE'
    EMAIL = 'DEFAULT_EMAIL'
    CHROMEDRIVER_PATH = 'DEFAULT_CHROMEDRIVER_PATH'
    APARTMENT_NUMBER = 'DEFAULT_APARTMENT_NUMBER'


class RegisterInfo:
    keys = RegisterKeys()

    def __init__(self, **kwargs):
        self.make = kwargs.get(self.keys.MAKE, RegisterDefaults.MAKE)
        self.model = kwargs.get(self.keys.MODEL, RegisterDefaults.MODEL)
        self.license_plate = kwargs.get(self.keys.LICENSE_PLATE, RegisterDefaults.LICENSE_PLATE)
        self.email = kwargs.get(self.keys.EMAIL, RegisterDefaults.EMAIL)
        self.chromedriver_path = kwargs.get(self.keys.CHROMEDRIVER_PATH, RegisterDefaults.CHROMEDRIVER_PATH)
        self.apartment_number = kwargs.get(self.keys.APARTMENT_NUMBER, RegisterDefaults.APARTMENT_NUMBER)


def register_2_park(
        chromedriver_path=None,
        make=None,
        model=None,
        license_plate=None,
        email=None,
        apartment_number=None
):

    # DOWNLOAD CHROMEDRIVER IF NEED TO
    exe_path = os.path.join(chromedriver_path, CHROMEDRIVER_EXE_NAME)
    if not file_exists(exe_path):
        download_chrome_driver(chromedriver_path)

    # ADD CHROMEDRIVER TO PATH
    os.environ["PATH"] += os.pathsep + exe_path

    # PERFORM UPGRADE
    driver = webdriver.Chrome(exe_path)
    driver.get("https://www.register2park.com/register")

    # FIRST PAGE
    property_name = driver.find_element_by_id("propertyName")
    property_name.send_keys("3500 Westlake")
    property_name.submit()
    # SECOND PAGE
    confirm_property = driver.find_element_by_id("confirmProperty")
    confirm_property.click()
    # THIRD PAGE
    driver.implicitly_wait(10)
    radio_btn = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/form/div/div/label/input')
    radio_btn.click()
    confirm_property_selection = driver.find_element_by_id("confirmPropertySelection")
    confirm_property_selection.click()
    # FOURTH PAGE
    registration_type_visitor = driver.find_element_by_id('registrationTypeVisitor')
    registration_type_visitor.click()
    # FIFTH PAGE - INFORMATION INPUT
    driver.implicitly_wait(10)
    vehicle_apt = driver.find_element_by_id('vehicleApt')
    vehicle_apt.click()
    vehicle_apt.send_keys(apartment_number)
    vehicle_make = driver.find_element_by_id('vehicleMake')
    vehicle_make.click()
    vehicle_make.send_keys(make)
    vehicle_model = driver.find_element_by_id('vehicleModel')
    vehicle_model.click()
    vehicle_model.send_keys(model)
    vehicle_license_plate = driver.find_element_by_id('vehicleLicensePlate')
    vehicle_license_plate.click()
    vehicle_license_plate.send_keys(license_plate)
    vehicle_license_plate_confirm = driver.find_element_by_id('vehicleLicensePlateConfirm')
    vehicle_license_plate_confirm.click()
    vehicle_license_plate_confirm.send_keys(license_plate)
    vehicle_information = driver.find_element_by_id('vehicleInformation')
    vehicle_information.click()
    # SIXTH PAGE - EMAIL CONFIRMATION
    email_confirmation = driver.find_element_by_id('email-confirmation')
    email_confirmation.click()
    email_confirmation_email_view = driver.find_element_by_id('emailConfirmationEmailView')
    email_confirmation_email_view.click()
    email_confirmation_email_view.send_keys(email)
    email_confirmation_send_view = driver.find_element_by_id('email-confirmation-send-view')
    email_confirmation_send_view.click()

    driver.close()
    driver.quit()


if __name__ == '__main__':
    from App_3500ParkingLogin.ParkingLoginApp import *
    yes_or_no = 'n'
