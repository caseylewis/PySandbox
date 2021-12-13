import logging
from abc import abstractmethod
import sqlite3
import json


class ColumnTypes:
    NULL = "NULL"
    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"


DEF_INTEGER_VAL = 0
DEF_REAL_VAL = 0
DEF_TEXT_VAL = ""
DEF_BLOB_VAL = ""

DEF_VAL_MAP = {
    ColumnTypes.NULL: 0,
    ColumnTypes.INTEGER: DEF_INTEGER_VAL,
    ColumnTypes.REAL: DEF_REAL_VAL,
    ColumnTypes.TEXT: DEF_TEXT_VAL,
    ColumnTypes.BLOB: DEF_BLOB_VAL,
}

DB_LIST_SEPARATOR = '**'
DB_LIST_BLANK_ENTRY = ''


TABLE_NAME_KEY = 'table_name'
COLUMN_MAP_KEY = 'column_map'
COLUMN_NAME_INDEX = 0
COLUMN_TYPE_INDEX = 1

# table_info_dict = {
#     TABLE_NAME_KEY: "",
#     COLUMN_MAP_KEY: {
#         index: (column_name, column_type),
#     },
# }


def db_debug_test_statement(conn, sql):
    data, error = __db_execute_and_get_output(conn, sql)
    return data, error


def db_row_dict_to_tuple(dict_to_convert):
    entry_tuple = tuple()
    for col_index in range(len(dict_to_convert)):
        entry_tuple += (dict_to_convert[col_index],)

    return entry_tuple


def db_list_to_string(row_list):
    list_string = ""
    list_len = len(row_list)
    for index in range(list_len):
        list_string += str(row_list[index])
        if index < list_len-1:
            list_string += DB_LIST_SEPARATOR
    print(list_string)
    return list_string


###########################################################
# READ OPERATIONS
###########################################################


def db_check_table_exists(conn, table_name):
    sql = """ SELECT name FROM sqlite_master WHERE type='table' AND name='{}'; """.format(table_name)

    data, error = __db_execute_and_get_output(conn, sql)
    table_exists = False
    try:
        if data[0][0] == table_name:
            table_exists = True
    except IndexError:
        pass
    except Exception as e:
        error = e.args
    return table_exists, error


def db_get_table_column_info_dict(conn, table_name):
    action = 'PRAGMA table_info'
    sql = """ {} ({}); """.format(action, table_name)

    data, error = __db_execute_and_get_output(conn, sql)

    column_info_dict = {}
    if error is None:
        for column_info_tup in data:
            col_index, col_name, col_type, null, null, null = column_info_tup
            column_info_dict[col_index] = (col_name, col_type)
    return column_info_dict, error


def db_select_all_from_table(conn, table_info_dict):
    table_name = table_info_dict[TABLE_NAME_KEY]

    # SET UP SQL STATEMENT WITH FORMAT """ SELECT * FROM {TABLE_NAME} """
    action = 'SELECT * FROM'
    sql = """ {} {} """.format(action, table_name)

    data, error = __db_execute_and_get_output(conn, sql)
    row_dict = {}
    table_columns = table_info_dict[COLUMN_MAP_KEY]
    column_count = len(table_columns)
    if error is None:
        row_index = 0
        # ITERATE THROUGH ROWS IN DATA
        for row in data:
            row_data_dict = {}
            # COPY OVER COLUMNS FROM TABLE_COLUMNS INTO ROW_DATA_DICT'S ROW DICT
            for col_index in range(column_count):
                row_val = row[col_index]
                row_data_dict[col_index] = row_val
                col_index += 1
            row_dict[row_index] = row_data_dict
            row_index += 1

    return row_dict, error


def db_select_all_where_first_column_equals(conn, table_info_dict, first_column_val):
    table_name = table_info_dict[TABLE_NAME_KEY]

    # SET UP SQL STATEMENT WITH FORMAT """ SELECT * FROM {TABLE_NAME} """
    action = 'SELECT * FROM'
    sql = """ {} {} WHERE {} == '{}' """.format(action, table_name, table_info_dict[COLUMN_MAP_KEY][0][0], first_column_val)

    data, error = __db_execute_and_get_output(conn, sql)
    row_dict = {}
    table_columns = table_info_dict[COLUMN_MAP_KEY]
    column_count = len(table_columns)
    if error is None:
        row_index = 0
        # ITERATE THROUGH ROWS IN DATA
        for row in data:
            row_data_dict = {}
            # COPY OVER COLUMNS FROM TABLE_COLUMNS INTO ROW_DATA_DICT'S ROW DICT
            for col_index in range(column_count):
                row_val = row[col_index]
                row_data_dict[col_index] = row_val
                col_index += 1
            row_dict[row_index] = row_data_dict
            row_index += 1

    return row_dict, error


###########################################################
# WRITE OPERATIONS
###########################################################


def db_alter_table(conn, table_info_dict):
    table_name = table_info_dict[TABLE_NAME_KEY]
    columns = table_info_dict[COLUMN_MAP_KEY]


def db_drop_table(conn, table_name):
    action = 'DROP TABLE'
    sql = """ {} {} """.format(action, table_name)

    data, error = __db_execute_and_get_output(conn, sql)
    if error is not None:
        conn.commit()
    return data, error


def db_create_table(conn, table_info_dict):
    table_name = table_info_dict[TABLE_NAME_KEY]
    columns = table_info_dict[COLUMN_MAP_KEY]

    # SET UP SQL STATEMENT WITH FORMAT """ CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({COLUMNS AND TYPES}); """
    action = 'CREATE TABLE IF NOT EXISTS'
    columns_str = __get_columns_and_types_str(columns)
    sql = """ {} {} ({}); """.format(action, table_name, columns_str)

    data, error = __db_execute_and_get_output(conn, sql)
    if error is not None:
        conn.commit()
    return data, error


def db_insert_into_table(conn, table_info_dict, val_tuple):
    table_name = table_info_dict[TABLE_NAME_KEY]
    columns = table_info_dict[COLUMN_MAP_KEY]

    # SET UP SQL STATEMENT WITH FORMAT """ INSERT INTO {TABLE_NAME}({COLUMN_NAMES}) VALUES({QUESTIONS_MARK_COUNT}) """
    action = 'INSERT INTO'
    column_names = __get_column_names(columns)
    question_mark_count = __get_question_mark_count(columns)
    sql = """ {} {} ({}) VALUES({}) """.format(action, table_name, column_names, question_mark_count)

    data, error = __db_execute_and_get_output(conn, sql, val_tuple)
    if error is not None:
        conn.commit()
    return data, error


def db_update_where_first_column_equals(conn, table_info_dict, val_tuple, first_column_val):
    table_name = table_info_dict[TABLE_NAME_KEY]
    col_dict = table_info_dict[COLUMN_MAP_KEY]

    # SET UP SQL STATEMENT WITH FORMAT """ INSERT INTO {TABLE_NAME}({COLUMN_NAMES}) VALUES({QUESTIONS_MARK_COUNT}) """
    action = 'UPDATE'
    set_columns = __db_get_set_columns_and_values(col_dict, val_tuple)
    where_condition = __db_get_first_column_where_condition(col_dict, first_column_val)
    sql = """ {} {} SET {} {} """.format(action, table_name, set_columns, where_condition)

    data, error = __db_execute_and_get_output(conn, sql)
    if error is not None:
        conn.commit()
    return data, error


def db_delete_where_first_column_equals(conn, table_info_dict, first_column_val):
    table_name = table_info_dict[TABLE_NAME_KEY]
    col_dict = table_info_dict[COLUMN_MAP_KEY]

    # SET UP SQL STATEMENT WITH FORMAT """ INSERT INTO {TABLE_NAME}({COLUMN_NAMES}) VALUES({QUESTIONS_MARK_COUNT}) """
    action = 'DELETE FROM'
    where_condition = __db_get_first_column_where_condition(col_dict, first_column_val)
    sql = """ {} {} {} """.format(action, table_name, where_condition)

    data, error = __db_execute_and_get_output(conn, sql)
    if error is not None:
        conn.commit()
    return data, error


def db_delete_all_from_table(conn, table_info_dict):
    table_name = table_info_dict[TABLE_NAME_KEY]

    # SET UP SQL STATEMENT WITH FORMAT """ DELETE FROM {TABLE_NAME} """
    action = 'DELETE FROM'
    sql = """ {} {} """.format(action, table_name)

    data, error = __db_execute_and_get_output(conn, sql)
    if error is not None:
        conn.commit()
    return data, error


###########################################################
# HELPER FUNCTIONS
###########################################################

def __db_get_first_column_where_condition(col_dict, first_col_val):
    first_col_name, col_type, col_length = col_dict[0]
    where_condition = """WHERE {} = '{}'""".format(first_col_name, first_col_val)
    return where_condition


def __db_get_set_columns_and_values(col_dict, set_tuple):
    set_string = ""
    separator = ", "
    for col_index in range(len(col_dict)):
        col_name, col_type, col_length = col_dict[col_index]
        set_val = set_tuple[col_index]
        next_val_str = "{} = '{}'{}".format(col_name, set_val, separator)
        set_string += next_val_str
    for x in range(len(separator)):
        set_string = set_string[:-1]
    return set_string


def __db_execute_and_get_output(conn, sql, tuple_values=None):
    """
    Most important function for db interfacing. Executes sql statement with option of tuple_values and returns
    data or error message.
    :param conn: sqlite3 connection
    :param sql: sql statement to execute
    :param tuple_values: tuple of values to execute in an insert statement etc..
    :return: data: rows returned from sql statement OR error: error received from sql execute
    """
    data = None
    error = None

    cursor = conn.cursor()
    # CONNECTION EXISTS
    if cursor is not None:
        logging.debug("sending sql: {}".format(sql))
        try:
            # SENDING A TUPLE FOR SELECT STATEMENT
            if tuple_values is None:
                cursor.execute(sql)
                data = cursor.fetchall()
            # SENDING SIMPLE SQL STATEMENT
            else:
                cursor.execute(sql, tuple_values)
                data = cursor.fetchall()
        except sqlite3.OperationalError:
            error = "OperationalError in statement: '''{}'''".format(sql)
    # CONNECTION FAILED
    else:
        error = "Could not connect to database."

    return data, error


def __get_columns_and_types_str(columns_dict):
    """
    Get a formatted string of columns and types for the create table sql statement.
    :param columns_dict:
    :return: columns_str FORMAT "{column_name} {column_type}, {column_name} {column_type}, ... {column_name} {column_type}"
    """
    # GET COLUMNS FROM COLUMNS DICT AND FORMAT STRING WITH COLUMN NAME AND COLUMN TYPE
    columns_str = ""
    current_column = 0
    last_column_found = False
    while not last_column_found:
        col_info_tup = columns_dict.get(current_column)
        if col_info_tup is not None:
            col_name, col_type, col_length = col_info_tup
            columns_str += "{} {},".format(col_name, col_type)
        else:
            last_column_found = True
        current_column += 1
    # REMOVE FINAL COMMA
    columns_str = columns_str[:-1]

    return columns_str


def __get_column_names(columns_dict):
    """
    Get a formatted string of column names for insert sql statement
    :param columns_dict:
    :return: columns_name_str FORMAT "{column_name}, {column_name}, ... {column_name}"
    """
    # GET COLUMN NAMES FROM COLUMNS DICT AND FORMAT STRING WITH COLUMN NAME
    columns_name_str = ""
    current_column = 0
    last_column_found = False
    while not last_column_found:
        col_info_tup = columns_dict.get(current_column)
        if col_info_tup is not None:
            col_name, col_type, col_length = col_info_tup
            columns_name_str += "{},".format(col_name)
        else:
            last_column_found = True
        current_column += 1
    # REMOVE FINAL COMMA
    columns_name_str = columns_name_str[:-1]

    return columns_name_str


def __get_question_mark_count(columns_dict):
    # GET QUESTIONS MARKS FOR INSERT SQL STATEMENT
    question_mark_str = ""
    column_count = len(columns_dict)
    for q in range(column_count):
        question_mark_str += "?,"
    question_mark_str = question_mark_str[:-1]

    return question_mark_str


class DBTableInterface:

    @property
    @abstractmethod
    def table_str(self):
        pass

    # @property
    # @abstractmethod
    # def table_info_dict(self):
    #     pass

    @property
    def __mismatch_index(self):
        return -1

    def __init__(self, db_conn, table_info_dict):
        self.__db_conn = db_conn
        self.table_info_dict = table_info_dict

    ###########################################################
    # WRITE OPERATIONS
    ###########################################################

    def db_create_table(self):
        data, error = db_create_table(self.__db_conn, self.table_info_dict)
        return data, error

    def db_insert_into_table(self, val_tuple):
        data, error = db_insert_into_table(self.__db_conn, self.table_info_dict, val_tuple)
        return data, error

    def db_delete_all_from_table(self):
        data, error = db_delete_all_from_table(self.__db_conn, self.table_info_dict)
        return data, error

    def db_drop_table(self):
        return db_drop_table(self.__db_conn, self.table_info_dict[TABLE_NAME_KEY])

    def db_table_init(self):
        table_exists, error = db_check_table_exists(self.__db_conn, self.table_info_dict[TABLE_NAME_KEY])
        if error is not None:
            logging.error(error)
        else:
            if not table_exists:
                self.db_create_table()
            else:
                other_table_col_info_dict, error = self.db_get_table_column_info_dict()
                table_is_match = self.check_tables_match(other_table_col_info_dict)
                if not table_is_match:
                    perform_alter = True
                    if perform_alter:
                        output, error = self.db_alter_table(other_table_col_info_dict)
                        if error is not None:
                            logging.error(error)
                    else:
                        return
                else:
                    return

    def db_alter_table(self, old_table_col_dict):
        data = {}
        error = None
        # SET UP OTHER_TABLE_INFO_DICT, THIS IS NEEDED TO DO THE DB_SELECT_ALL
        other_table_info_dict = dict()
        other_table_info_dict[TABLE_NAME_KEY] = self.table_info_dict[TABLE_NAME_KEY]
        other_table_info_dict[COLUMN_MAP_KEY] = old_table_col_dict

        other_table_row_data_dict, error = db_select_all_from_table(self.__db_conn, other_table_info_dict)

        # COMPARE EACH ROW AND PUT MATCHING COLUMNS WHERE THEY BELONG
        col_compare_list = self.__get_column_compare_list(old_table_col_dict)

        # TAKE THE CURRENT DATA FROM THE OLD TABLE
        temp_row_data_dict = self.__get_joined_row_data_dict(other_table_row_data_dict, col_compare_list)

        self.db_drop_table()
        self.db_create_table()

        # INSERT EACH ROW BACK INTO THE NEW ALTERED TABLE
        for col_index, col_dict in temp_row_data_dict.items():
            val_tuple = db_row_dict_to_tuple(col_dict)
            data, error = self.db_insert_into_table(val_tuple)
            if error is not None:
                break

        return data, error

    def db_update_where_first_column_equals(self, val_tuple, first_column_val):
        data, error = db_update_where_first_column_equals(self.__db_conn, self.table_info_dict, val_tuple, first_column_val)
        return data, error

    def db_delete_where_first_column_equals(self, first_column_val):
        data, error = db_delete_where_first_column_equals(self.__db_conn, self.table_info_dict, first_column_val)
        return data, error

    ###########################################################
    # READ OPERATIONS
    ###########################################################

    def db_select_all_from_table(self):
        """
        Return all rows from the table associated with this object
        :return: row_dict, error
        """
        row_dict, error = db_select_all_from_table(self.__db_conn, self.table_info_dict)
        return row_dict, error

    def db_select_all_where_first_column_equals(self, first_column_val):
        row_dict, error = db_select_all_where_first_column_equals(self.__db_conn, self.table_info_dict, first_column_val)
        return row_dict, error

    def db_get_table_column_info_dict(self):
        col_info_dict, error = db_get_table_column_info_dict(self.__db_conn, self.table_info_dict[TABLE_NAME_KEY])
        return col_info_dict, error

    def db_debug_test_statement(self, sql):
        output, error = db_debug_test_statement(self.__db_conn, sql)
        return output, error

    def db_check_table_exists(self):
        table_exists, error = db_check_table_exists(self.__db_conn, self.table_info_dict[TABLE_NAME_KEY])
        return table_exists, error

    def __get_joined_row_data_dict(self, other_table_row_data_dict, col_compare_list):
        temp_row_data_dict = {}
        for row_index, col_dict in other_table_row_data_dict.items():
            temp_row_data_dict[row_index] = {}
            for col_index in range(len(col_compare_list)):
                col_index_to_get_data_from = col_compare_list[col_index]
                if col_index_to_get_data_from == self.__mismatch_index:
                    # INSERT DEFAULT VALUE FOR THAT TYPE
                    col_type = self.table_info_dict[COLUMN_MAP_KEY][col_index][COLUMN_TYPE_INDEX]
                    def_val = DEF_VAL_MAP[col_type]
                    temp_row_data_dict[row_index][col_index] = def_val
                else:
                    temp_row_data_dict[row_index][col_index] = other_table_row_data_dict[row_index][col_index_to_get_data_from]

        return temp_row_data_dict

    @staticmethod
    def __debug_output_row_col_from_table(row_data_dict):
        print("outputting all data from dict below:")
        for row_index, col_dict in row_data_dict.items():
            print("ROW: ", row_index)
            for col_index, col_val in col_dict.items():
                print("    COL: {} '{}'".format(col_index, col_val))

    def __get_column_compare_list(self, other_table_col_dict):
        table_col_dict = self.table_info_dict[COLUMN_MAP_KEY]
        table_col_count = len(table_col_dict)
        other_table_col_count = len(other_table_col_dict)
        col_compare_list = []

        # ITERATE THROUGH ALL TABLE COLUMNS
        for col_index in range(table_col_count):
            # ITERATE THROUGH ALL OTHER TABLE COLUMNS
            for other_col_index in range(other_table_col_count):
                # IF NAMES MATCH, APPEND OTHER_COL_INDEX TO COL_COMPARE_LIST
                names_match = table_col_dict[col_index][COLUMN_NAME_INDEX] == other_table_col_dict[other_col_index][COLUMN_NAME_INDEX]
                types_match = table_col_dict[col_index][COLUMN_TYPE_INDEX] == other_table_col_dict[other_col_index][COLUMN_TYPE_INDEX]
                if names_match and types_match:
                    col_compare_list.append(other_col_index)
                    break  # DON'T KEEP SEARCHING, COLUMNS CAN ONLY MATCH ONCE
            # IF NOTHING WAS APPENDED, IT MEANS THERE WAS A MISMATCH, APPEND THAT TO COL_COMPARE_LIST
            if not((0 <= col_index) and (col_index < len(col_compare_list))):
                col_compare_list.append(self.__mismatch_index)

        return col_compare_list

    def check_tables_match(self, other_table_col_dict):
        """
        Checks if the table column dicts are a match
        :param other_table_col_dict: The other table column dict to compare to
        :return: True if match, False if not
        """
        table_is_match = True

        this_table_col_dict = self.table_info_dict[COLUMN_MAP_KEY]

        col_count = len(this_table_col_dict)
        other_col_count = len(other_table_col_dict)

        # IF NUMBER OF COLUMNS DON'T MATCH RETURN FALSE
        if col_count != other_col_count:
            table_is_match = False

        # CHECK EACH COLUMN NUMBER, IF DIFFERENT RETURN FALSE
        for col_index in range(col_count):
            if this_table_col_dict[COLUMN_NAME_INDEX][:2] != other_table_col_dict[COLUMN_NAME_INDEX][:2] or this_table_col_dict[COLUMN_TYPE_INDEX][:2] != other_table_col_dict[COLUMN_TYPE_INDEX][:2]:
                table_is_match = False

        return table_is_match


# class AbstractDBTable:
#
#     @classmethod
#     @abstractmethod
#     def table_name(cls):
#         pass
#
#     @classmethod
#     @abstractmethod
#     def table_columns_dict(cls):
#         pass
#
#     @classmethod
#     def table_info_dict(cls):
#         table_info_dict = {
#             TABLE_NAME_KEY: cls.table_name.lower(),
#             COLUMN_MAP_KEY: cls.table_columns_dict,
#         }
#         return table_info_dict


# class AbstractTableColumn:
#     """
#     Set it up like:
#         table_columns_dict = {
#             0: AbstractTableColumn('test_col', ColumnTypes.TEXT, 20)
#         }
#     """
#     def __init__(self, column_name, type_, length):
#         self.column_name = column_name
#         self.type_ = type_
#         self.length = length
#
#     def __new__(cls, *args, **kwargs):
#         return cls.column_name, cls.type_, cls.length


def AbstractTableColumn(column_name, type_, length):
    return column_name, type_, length


class AbstractDBTable:

    @classmethod
    @abstractmethod
    def table_name(cls):
        pass

    @classmethod
    @abstractmethod
    def table_columns_dict(cls):
        pass

    @classmethod
    def table_info_dict(cls):
        table_info_dict = {
            TABLE_NAME_KEY: cls.table_name.lower(),
            COLUMN_MAP_KEY: cls.table_columns_dict,
        }
        return table_info_dict

    def __init__(self, table_name, table_columns_dict):
        self.table_name = table_name
        self.table_columns_dict = table_columns_dict

    @staticmethod
    @abstractmethod
    def get_insert_tuple(**kwargs):
        pass


if __name__ == '__main__':
    from Libs.OSLib.os_helper import *

    # EXAMPLE OF ABSTRACTDBTABLE
    class TestTableInfo(AbstractDBTable):
        table_name = "TEST_TABLE"
        table_columns_dict = {
            0: AbstractTableColumn('first_column', ColumnTypes.TEXT, 20),
            1: AbstractTableColumn('second_column', ColumnTypes.TEXT, 20),
            2: AbstractTableColumn('third_column', ColumnTypes.TEXT, 20),
        }

        @staticmethod
        def get_insert_tuple(first_column, second_column, third_column):
            return first_column, second_column, third_column


    def output_select_all_data(row_dict, error):
        if error is not None:
            print("Error: [ {} ]".format(error))
        for row, column in row_dict.items():
            print(row)
            for column_name, value in column.items():
                print('\t', column_name, value)


    # GET CURRENT DIRECTORY
    cwd = os.getcwd()
    TEST_DB_FILE = '{}\\test.db'.format(cwd)

    # DELETE DB IF ONE EXISTS
    file_delete(TEST_DB_FILE)

    # CREATE DB FILE
    file_create(TEST_DB_FILE)

    # CONNECT TO DB
    db_conn = sqlite3.connect(TEST_DB_FILE)

    # CREATE COLUMNS
    table_columns_dict = {
        0: AbstractTableColumn('first_column', ColumnTypes.TEXT, 20),
        1: AbstractTableColumn('second_column', ColumnTypes.TEXT, 20),
        2: AbstractTableColumn('third_column', ColumnTypes.TEXT, 20),
    }

    # CREATE DB TABLE INTERFACE
    test_table_db_interface = DBTableInterface(db_conn, TestTableInfo.table_info_dict())

    # CREATE TABLE
    test_table_db_interface.db_create_table()

    # INSERT ROWS
    test_table_db_interface.db_insert_into_table(TestTableInfo.get_insert_tuple('one', 'two', 'three'))
    test_table_db_interface.db_insert_into_table(TestTableInfo.get_insert_tuple('4', '5', '6'))

    # SELECT ALL AND OUTPUT
    print("Printing all data from [ {} ]".format(test_table_db_interface.table_info_dict[TABLE_NAME_KEY]))
    output_select_all_data(*test_table_db_interface.db_select_all_from_table())

    # DISCONNECT DB
    db_conn.close()

    # DELETE DB FILE
    file_delete(TEST_DB_FILE)

