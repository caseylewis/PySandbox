import os
import requests
import zipfile
import shutil
from subprocess import Popen, PIPE, STDOUT
import platform
from Libs.OSLib.os_helper import *
import signal


def __get_chrome_version_linux():
    chrome_version = None
    cmd = 'google-chrome --version'
    try:
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)#, close_fds=True)
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
                return dir_name


def get_chrome_version():
    if platform.system() == 'Linux':
        return __get_chrome_version_linux()
    elif platform.system() == 'Windows':
        return __get_chrome_version_windows()


def download_chrome_driver(dir):
    # TEMP DIRECTORY STARTS WITH DESKTOP PATH
    temp_dir = os.path.join(dir, 'tempdownload')
    # CREATE TEMP DIR AND CHANGE TO IT
    if not os.path.exists(temp_dir):
        dir_create(temp_dir)
        # os.umask(0)
        # os.mkdir(temp_dir, mode=777)
        # os.chmod(temp_dir, 777)
    # os.chdir(temp_dir)

    chrome_version = get_chrome_version()
    # SET UP CHROME VERSION WITH JUST MAJOR, MINOR, AND BUILD VERSION
    major, minor, build_version, remove_version = chrome_version.split('.')

    # CHROME DRIVER DOWNLOAD LINK IS THE CHROME VERSION MINUS THE LAST PART OF THE VERSION NUMBER
    chrome_driver_latest_release_link = r'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}.{}.{}'.format(
        major, minor, build_version)

    # GET LATEST VERSION TO DOWNLOAD THE CORRECT ZIP FILE
    r = requests.get(chrome_driver_latest_release_link, allow_redirects=True)
    latest_version = r.content.decode('ascii')

    running_os = platform.system()
    if running_os == 'Linux':
        zip_file_name = 'chromedriver_linux64.zip'
        chrome_driver_exe_name = 'chromedriver'
    elif running_os == 'Windows':
        zip_file_name = 'chromedriver_win32.zip'
        chrome_driver_exe_name = 'chromedriver.exe'
    else:
        raise Exception("OS not supported")

    # FINALLY GET THE ACTUALLY DOWNLOAD LINK
    chrome_driver_zip_download_link = 'https://chromedriver.storage.googleapis.com/{}/{}'.format(
        latest_version, zip_file_name)

    # DOWNLOAD ZIP FILE TO TEMP DIRECTORY
    r = requests.get(chrome_driver_zip_download_link, allow_redirects=True)
    # zip_file_name = 'chromedriver_win32.zip'
    zip_location = os.path.join(temp_dir, zip_file_name) #r"{}\{}".format(temp_dir, zip_file_name)
    write_file = open(zip_location, 'wb')
    write_file.write(r.content)

    # EXTRACT ZIP FILE
    with zipfile.ZipFile(zip_location, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
        zip_ref.close()

    # MOVE CHROMEDRIVER TO CORRECT APP DIRECTORY
    chromedriver_exe_location = os.path.join(temp_dir, chrome_driver_exe_name)
    app_chromedriver_exe_location = os.path.join(dir, chrome_driver_exe_name)
    # IF CHROMEDRIVER EXISTS IN APP LOCATION, IT MUST BE DELETED BEFORE BEING MOVED OVER
    if os.path.exists(app_chromedriver_exe_location):
        os.remove(app_chromedriver_exe_location)
        print("removed current chromedriver")
    # MOVE CHROMEDRIVER TO APP LOCATION
    os.rename(chromedriver_exe_location, app_chromedriver_exe_location)
    os.chmod(app_chromedriver_exe_location, 0o771)

    # CHANGE DIR BACK TO APP DIR SO THAT CHROMEDRIVER WILL BE USED PROPERLY
    os.chdir(dir)
    # DELETE ALL FROM TEMP DIR
    delete_all_from_dir(temp_dir)
    dir_remove(temp_dir)


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
