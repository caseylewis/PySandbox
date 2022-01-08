

class UserKeys:
    NAME = 'Name'
    MAKE = 'make'
    MODEL = 'model'
    LICENSE_PLATE = 'license_plate'
    EMAIL = 'email'
    all_keys = [
        NAME,
        MAKE,
        MODEL,
        LICENSE_PLATE,
        EMAIL,
    ]


class User(dict):
    keys = UserKeys

    @property
    def name(self):
        return self[self.keys.NAME]

    @name.setter
    def name(self, val):
        self[self.keys.NAME] = val

    def __init__(self, user_dict):
        super().__init__()
        for key, value in user_dict.items():
            self[key] = value


test_user_list = list()
test_user_list.append(User({
        UserKeys.NAME: "Casey",
        UserKeys.MAKE: "Toyota",
        UserKeys.MODEL: "Avalon",
        UserKeys.LICENSE_PLATE: "CZX0399",
        UserKeys.EMAIL: "caseyray.lewis@gmail.com"
    }))
for x in range(9):
    user_index = str(x+1)
    user_dict = {
        UserKeys.NAME: "User {}".format(user_index),
        UserKeys.MAKE: "Make {}".format(user_index),
        UserKeys.MODEL: "Model {}".format(user_index),
        UserKeys.LICENSE_PLATE: "License {}".format(user_index),
        UserKeys.EMAIL: "Email {}".format(user_index)
    }
    test_user_list.append(User(user_dict))

