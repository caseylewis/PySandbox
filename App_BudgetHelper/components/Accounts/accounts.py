from App_BudgetHelper.AbstractData import *


class AccountKeys(AbstractKeys):
    NAME = AbstractObjCommonKeys.NAME
    ACC_NUM = 'Account #'
    ROUT_NUM = 'Routing #'
    DESC = 'Description'

    all_keys = [
        NAME,
        ACC_NUM,
        ROUT_NUM,
        DESC
    ]

    required_keys = [
        NAME,
        ACC_NUM,
        ROUT_NUM,
    ]

    def __init__(self):
        super().__init__()


class AccountIndices(AbstractIndices):
    NAME = 0
    ACC_NUM = 1
    ROUT_NUM = 2
    DESC = 3

    all_indices = [
        NAME,
        ACC_NUM,
        ROUT_NUM,
        DESC
    ]

    def __init__(self):
        super().__init__()


class Account(AbstractDictBasedDataObject):
    object_name = "Account"
    keys = AccountKeys
    idxs = AccountIndices

    # NAME
    @property
    def name(self):
        return self[self.keys.NAME]

    @name.setter
    def name(self, val):
        self[self.keys.NAME] = val

    # ACCOUNT NUM
    @property
    def account_num(self):
        return self[self.keys.ACC_NUM]

    @account_num.setter
    def account_num(self, val):
        self[self.keys.ACC_NUM] = val

    # ROUTE NUM
    @property
    def route_num(self):
        return self[self.keys.ROUT_NUM]

    @route_num.setter
    def route_num(self, val):
        self[self.keys.ROUT_NUM] = val

    # DESCRIPTION
    @property
    def description(self):
        return self[self.keys.DESC]

    @description.setter
    def description(self, val):
        self[self.keys.DESC] = val

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def default_values(self):
        self[self.keys.DESC] = self.get(self.keys.DESC, "Not Set")

    def output_account(self):
        print("{}\n"
              "\t{}".format(self.name, self.description))


__test_account_dict = {
    Account.keys.NAME: 'test',
    Account.keys.ACC_NUM: '2121243321',
    Account.keys.ROUT_NUM: '23423432',
    # Account.keys.DESC: 'Test Description',
}

test_account = Account(**__test_account_dict)


if __name__ == '__main__':
    print(test_account)
