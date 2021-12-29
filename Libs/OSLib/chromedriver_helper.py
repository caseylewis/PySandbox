import platform
import time
import zipfile
from subprocess import PIPE, Popen, STDOUT

import requests

from Libs.OSLib.os_helper import *

# OS DEPENDENT VARIABLES
running_os = platform.system()
if running_os == 'Linux':
    CHROMEDRIVER_ZIP_NAME = 'chromedriver_linux64.zip'
    CHROMEDRIVER_EXE_NAME = 'chromedriver'
elif running_os == 'Windows':
    CHROMEDRIVER_ZIP_NAME = 'chromedriver_win32.zip'
    CHROMEDRIVER_EXE_NAME = 'chromedriver.exe'
else:
    raise Exception("OS not supported")


def __get_chrome_version_linux():
    chrome_version = None
    cmd = 'google-chrome --version'
    try:
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        output = p.stdout.read().rstrip().decode()
        chrome_version = output.strip('Google Chrome')
        p.terminate()
        p.kill()
    except Exception as e:
        pass
    return chrome_version


def __get_chrome_version_windows():
    # DEFINE BOTH LIKELY LOCATIONS FOR CHROME TO BE INSTALLED ( Program Files or Program Files (x86) )
    chrome_dir_x86 = r'C:\Program Files (x86)\Google\Chrome\Application'
    chrome_dir = r'C:\Program Files\Google\Chrome\Application'

    target_dir = None

    # GET TARGET PATH BASED ON WHICH EXISTS
    if os.path.exists(chrome_dir_x86):
        target_dir = chrome_dir_x86
    elif os.path.exists(chrome_dir):
        target_dir = chrome_dir

    # GET THE ACTUAL VERSION PATH
    if target_dir is not None:
        walk_return = os.scandir(target_dir)
        for dir_item in walk_return:
            dir_name = dir_item.name
            if dir_name == "SetupMetrics":
                continue
            full_dir_item_path = target_dir + r"\{}".format(dir_item.name)
            # THE VERSION WILL HAVE IT'S OWN DIRECTORY, SO CHECK THEM ALL
            if os.path.isdir(full_dir_item_path):
                walk_return.close()
                return dir_name


def get_chrome_version():
    if platform.system() == 'Linux':
        return __get_chrome_version_linux()
    elif platform.system() == 'Windows':
        return __get_chrome_version_windows()


def download_chrome_driver(dir):
    # TEMP DIRECTORY STARTS WITH DESKTOP PATH
    temp_dir = os.path.join(dir, 'tempdownload')
    dir_create(temp_dir)

    # SET UP CHROME VERSION WITH JUST MAJOR, MINOR, AND BUILD VERSION
    chrome_version = get_chrome_version()
    major, minor, build_version, remove_version = chrome_version.split('.')

    # CHROME DRIVER DOWNLOAD LINK IS THE CHROME VERSION MINUS THE LAST PART OF THE VERSION NUMBER
    chrome_driver_latest_release_link = r'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}.{}.{}'.format(
        major, minor, build_version)

    # GET LATEST VERSION TO DOWNLOAD THE CORRECT ZIP FILE
    r = requests.get(chrome_driver_latest_release_link, allow_redirects=True)
    latest_version = r.content.decode('ascii')

    # FINALLY GET THE ACTUALLY DOWNLOAD LINK
    chrome_driver_zip_download_link = 'https://chromedriver.storage.googleapis.com/{}/{}'.format(
        latest_version, CHROMEDRIVER_ZIP_NAME)

    # DOWNLOAD ZIP FILE TO TEMP DIRECTORY
    r = requests.get(chrome_driver_zip_download_link, allow_redirects=True)
    zip_location = os.path.join(temp_dir, CHROMEDRIVER_ZIP_NAME)
    with open(zip_location, 'wb') as write_file:
        write_file.write(r.content)
        write_file.close()

    # EXTRACT ZIP FILE
    with zipfile.ZipFile(zip_location, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
        zip_ref.close()

    # MOVE CHROMEDRIVER TO CORRECT APP DIRECTORY
    chromedriver_exe_location = os.path.join(temp_dir, CHROMEDRIVER_EXE_NAME)
    app_chromedriver_exe_location = os.path.join(dir, CHROMEDRIVER_EXE_NAME)
    # IF CHROMEDRIVER EXISTS IN APP LOCATION, IT MUST BE DELETED BEFORE BEING MOVED OVER
    if os.path.exists(app_chromedriver_exe_location):
        os.remove(app_chromedriver_exe_location)
    # MOVE CHROMEDRIVER TO APP LOCATION
    os.rename(chromedriver_exe_location, app_chromedriver_exe_location)
    os.chmod(app_chromedriver_exe_location, 0o777)

    # DELETE ALL FROM TEMP DIR
    delete_all_from_dir(temp_dir)
    time.sleep(.1)
    dir_remove(temp_dir)
    time.sleep(.1)


def delete_all_from_dir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete '{}'. Reason: '{}'".format(file_path, e))


if __name__ == '__main__':
    # CHROME VERSION TEST
    # chrome_version = __get_chrome_version_linux()
    # print(chrome_version)

    print(get_chrome_version())

    # DOWNLOAD CHROME DRIVER TEST
    root_dir = os.getcwd()
    chromedriver_dir = os.path.join(root_dir, 'chromedriver')
    if not os.path.exists(chromedriver_dir):
        os.umask(0)
        os.mkdir(chromedriver_dir, mode=755)
    download_chrome_driver(chromedriver_dir)
