from selenium import webdriver
import os
from selenium.common.exceptions import WebDriverException
from Libs.OSLib.chromedriver_helper import *


parking_url = "https://www.register2park.com/register"

apt_desc = "3500 Westlake"  # Don't change this, it is an important input for the web page
apt_number = "1223"
email_address = 'caseyray.lewis@gmail.com'


def register_2_park(chromedriver_path=None, make=None, model=None, license_plate=None, email=None):
    """
    Attempt to register to park in the apartment complex.
    :param make:
    :param model:
    :param license_plate:
    :param email:
    :return: True if successful, False if unsuccessful
    """
    # CHECK OS FOR CHROMEDRIVER FILENAME, THEN DOWNLOAD CHROMEDRIVER IF NOT THERE
    running_os = platform.system()
    if running_os == 'Linux':
        chromedriver_exe_name = 'chromedriver'
    elif running_os == 'Windows':
        chromedriver_exe_name = 'chromedriver.exe'
    else:
        raise Exception("OS not supported: {}".format(running_os))
    exe_path = os.path.join(chromedriver_path, chromedriver_exe_name)
    if not file_exists(exe_path):
        download_chrome_driver(chromedriver_path)

    # ADD CHROMEDRIVER TO PATH
    os.environ["PATH"] += os.pathsep + exe_path

    # PERFORM UPGRADE
    driver = webdriver.Chrome(exe_path)
    driver.get(parking_url)

    # FIRST PAGE
    property_name = driver.find_element_by_id("propertyName")
    property_name.send_keys(apt_desc)
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
    vehicle_apt.send_keys(apt_number)
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

    register_kwargs = {
        # "name": "Natalie",
        "make": "Volkswagen",
        "model": "Jetta",
        "license": "MJH3932",
        "email": "caseyray.lewis@gmail.com"
    }
    chromedriver_path = PATH_CHROMEDRIVER

    register_2_park(**register_kwargs, chromedriver_path=chromedriver_path)

    # while yes_or_no == 'n':
    #     make = input("Make: ")
    #     model = input("Model: ")
    #     license_number = input("License Plate #: ")
    #     email = input("Email Address: ")
    #
    #     yes_or_no = input("\n"
    #                       "Make:            {}\n"
    #                       "Model:           {}\n"
    #                       "License Plate #: {}\n"
    #                       "Email Address:   {}\n"
    #                       "\n"
    #                       "If this is correct please enter 'y' or 'n' (Yes or No): ".format(make, model, license_number, email))
    #
    #     if yes_or_no == 'y':
    #         register_2_park(make, model, license_number, email)
