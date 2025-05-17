import sqlite3
import os
from unicodedata import category

from FinanceBot.data_categories_entries.data_categories import Categories


def create_database_if_it_does_not_exist(category: Categories):
    file_name = category.database_name_for_category()
    if not os.path.exists(file_name):
        conn = sqlite3.connect(category.database_name_for_category())
        c = conn.cursor()
        c.execute(f"CREATE TABLE {category.name} {category.string_to_create_database()}")
        c.close()


class sql_database_interface:
    def __init__(self, category: Categories):
        """
        Init the database interface with the category you want
        :param category: the category we want to open for the database
        """
        self.category = category
        create_database_if_it_does_not_exist(category)
        self.connection = sqlite3.connect(category.database_name_for_category())
        self.c = self.connection.cursor()

    def parse_line(self, tuple_values: tuple):
        """
        Parse the tuple line. The tuple has to have length equal to the number of elements one each row of the category
        :param tuple_values: the tuple values associated with the category of this database
        """
        assert len(tuple_values) == len(self.category.header)
        length_tuple = len(tuple_values)
        entry_to_add = "("
        for i in range(length_tuple - 1):
            entry_to_add += f"'{tuple_values[i].lower()}',"
        #add the last one
        entry_to_add += f"'{tuple_values[length_tuple -1].lower()}')"

        self.c.execute(f"INSERT INTO {self.category.name} VALUES {entry_to_add}")
        self.connection.commit()

    def filter_database(self, filter_lists):
        """
        Filter the rows of the database according to filter lists
        :param filter_lists: each list contains a number of filters for
        :return:
        """



    def close_connection(self):
        """
        Close the connection with the database
        """
        self.c.close()