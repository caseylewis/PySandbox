import os
import shutil
import stat


# DIRECTORY FUNCTIONS
def dir_create(path):
    """Checks if path exists, if not, creates it."""
    if not os.path.isdir(path):
        os.mkdir(path, mode=777)
        os.chmod(path, 0o777)
        # print(stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR)
        # os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


def dir_remove(path):
    # os.rmdir(path)
    shutil.rmtree(path)


def dir_exists(dirpath):
    return os.path.isdir(dirpath)


# FILE FUNCTIONS
def file_exists(filepath):
    return os.path.isfile(filepath)


def file_delete(filepath):
    if file_exists(filepath):
        os.remove(filepath)


def file_create(filepath):
    if not file_exists(filepath):
        f = open(filepath, 'x')
        os.chmod(filepath, 0o777)
        f.close()


class StandardAppDirStruct:
    def __init__(self, app_dir, app_name):
        self.app_dir = app_dir
        self.app_name = app_name

        # DATA DIRECTORY
        self.data_dir = os.path.join(self.app_dir, "data_{}".format(self.app_name))
        dir_create(self.data_dir)

        # SUB DIRECTORIES
        # LOGS DIRECTORY
        self.logs_dir = os.path.join(self.data_dir, "logs")
        dir_create(self.logs_dir)
        # RESOURCES DIRECTORY
        self.resources_dir = os.path.join(self.data_dir, "resources")
        dir_create(self.resources_dir)

    def clean_up(self):
        shutil.rmtree(self.data_dir)


if __name__ == '__main__':
    std_dir_struct = StandardAppDirStruct(os.getcwd(), "test_app")
    std_dir_struct.clean_up()
